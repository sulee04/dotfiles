#!/usr/bin/env python3
"""Install Linux release binaries and apply this repository with GNU Stow."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request

REPO = Path(__file__).resolve().parents[1]
PACKAGES = ('vim', 'zellij', 'codex', 'yazi', 'lazygit', 'shell')


def run(*args, cwd=None):
    subprocess.run([str(a) for a in args], cwd=cwd, check=True)


def fetch(url, output=None):
    request = urllib.request.Request(url, headers={'User-Agent': 'personal-dotfiles-setup'})
    with urllib.request.urlopen(request, timeout=120) as response:
        if output:
            with output.open('wb') as stream:
                shutil.copyfileobj(response, stream)
        else:
            return response.read()


class Setup:
    def __init__(self, args):
        self.args = args
        self.home = Path.home()
        self.local = self.home / '.local'
        self.bin = self.local / 'bin'
        self.backups = self.local / 'share/dotfiles-backups' / datetime.datetime.now(
            datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
        self.replaced = []

    def backup(self, path):
        if path.exists() or path.is_symlink():
            target = self.backups / path.relative_to(self.home)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(target))
            self.replaced.append((path, target))
            print(f'Backed up {path} to {target}', flush=True)

    def link(self, target, source):
        if target.is_symlink() and target.resolve() == source.resolve():
            return
        self.backup(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(source)

    def release(self, name, repository, asset, binaries):
        data = json.loads(fetch(f'https://api.github.com/repos/{repository}/releases/latest'))
        tag = data['tag_name']
        if not re.fullmatch(r'[\w.\-]+', tag):
            raise RuntimeError(f'Unexpected release tag: {tag}')
        asset = asset.format(version=tag.removeprefix('v'))
        entry = next((a for a in data['assets'] if a['name'] == asset), None)
        if not entry:
            raise RuntimeError(f'{repository} {tag} has no asset {asset}')
        dest = self.local / 'opt/dotfiles' / f'{name}-{tag}-{platform.machine()}'
        marker = dest / '.complete'
        if not marker.exists():
            with tempfile.TemporaryDirectory(prefix='dotfiles-download-') as temp:
                temp = Path(temp)
                archive = temp / asset
                print(f'Downloading {name} {tag}', flush=True)
                fetch(entry['browser_download_url'], archive)
                digest = entry.get('digest')
                if digest and digest.startswith('sha256:'):
                    with archive.open('rb') as stream:
                        checksum = hashlib.sha256()
                        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                            checksum.update(chunk)
                    if checksum.hexdigest() != digest.split(':', 1)[1]:
                        raise RuntimeError(f'Checksum mismatch: {asset}')
                extract = temp / 'extract'
                extract.mkdir()
                if asset.endswith('.zip'):
                    run('unzip', '-q', archive, '-d', extract)
                else:
                    run('tar', '-xzf', archive, '-C', extract)
                roots = list(extract.iterdir())
                source = roots[0] if len(roots) == 1 and roots[0].is_dir() else extract
                for executable, relative in binaries.items():
                    run(source / relative, '--version')
                dest.parent.mkdir(parents=True, exist_ok=True)
                if dest.exists():
                    self.backup(dest)
                shutil.move(str(source), str(dest))
                marker.touch()
        for executable, relative in binaries.items():
            self.link(self.bin / executable, dest / relative)

    def claude(self):
        if not (shutil.which('curl') or shutil.which('wget')):
            raise RuntimeError('Claude Code installation requires curl or wget')
        with tempfile.TemporaryDirectory(prefix='dotfiles-claude-') as temp:
            installer = Path(temp) / 'install.sh'
            fetch('https://claude.ai/install.sh', installer)
            run('bash', installer, 'stable')
        run(self.bin / 'claude', '--version')

    def stow(self):
        # GNU publishes its current stable source as stow-latest.tar.gz.
        with tempfile.TemporaryDirectory(prefix='dotfiles-stow-') as temp:
            temp = Path(temp)
            archive = temp / 'stow.tar.gz'
            fetch('https://ftp.gnu.org/gnu/stow/stow-latest.tar.gz', archive)
            run('tar', '-xzf', archive, '-C', temp)
            sources = list(temp.glob('stow-*/configure'))
            if len(sources) != 1:
                raise RuntimeError('Unexpected GNU Stow archive layout')
            source = sources[0].parent
            dest = self.local / 'opt/dotfiles' / source.name
            if not (dest / '.complete').exists():
                if dest.exists():
                    self.backup(dest)
                dest.parent.mkdir(parents=True, exist_ok=True)
                run(source / 'configure', f'--prefix={dest}', cwd=source)
                run('make', cwd=source)
                run('make', 'install', cwd=source)
                run(dest / 'bin/stow', '--version')
                (dest / '.complete').touch()
            self.link(self.bin / 'stow', dest / 'bin/stow')

    def configs(self):
        stow = shutil.which('stow')
        if not stow:
            raise RuntimeError('GNU Stow is required; run install.sh without --configs-only')
        # Back up only conflicting package leaves, retaining unrelated config files.
        saved = len(self.replaced)
        created = []
        try:
            for package in PACKAGES:
                root = REPO / package
                for source in list(root.rglob('*')):
                    if '.git' in source.relative_to(root).parts or source.name == '.stow-local-ignore':
                        continue
                    if source.is_dir() and not source.is_symlink():
                        continue
                    target = self.home / source.relative_to(root)
                    # Refuse a parent symlink into an unrelated directory.
                    for parent in reversed(target.parents):
                        if parent == self.home or self.home not in parent.parents:
                            continue
                        if parent.is_symlink() and not parent.resolve().is_relative_to(REPO):
                            raise RuntimeError(f'Config parent {parent} links outside this repository; relocate it before setup')
                    if target.exists() or target.is_symlink():
                        if target.resolve() == source.resolve():
                            if target.parent.resolve() == source.parent.resolve() or not target.is_symlink() or os.readlink(target) == os.path.relpath(source, target.parent):
                                continue
                        self.backup(target)
                    created.append(target)
            run(stow, '--dir', REPO, '--target', self.home, '--no-folding', '--simulate', '--restow', *PACKAGES, cwd=REPO)
            run(stow, '--dir', REPO, '--target', self.home, '--no-folding', '--restow', *PACKAGES, cwd=REPO)
        except Exception:
            for target in reversed(created):
                if target.is_symlink():
                    target.unlink()
            for original, backup in reversed(self.replaced[saved:]):
                if original.is_dir() and not original.is_symlink():
                    original.rmdir()
                original.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(backup), str(original))
            raise

    def main(self):
        if platform.system() != 'Linux':
            raise RuntimeError('This installer supports Linux; see README for prerequisites')
        arch = {'x86_64': 'x86_64', 'aarch64': 'aarch64', 'arm64': 'aarch64'}.get(platform.machine())
        if not arch:
            raise RuntimeError(f'Unsupported architecture: {platform.machine()}')
        if self.args.dry_run:
            print(f'Repository: {REPO}\nTarget: {self.home}\nArchitecture: {arch}')
            print('Would install stable Neovim, Yazi + ya, Zellij, Lazygit, GitHub CLI (gh), Codex, Claude Code, GNU Stow (unless --configs-only).')
            print('Would back up config conflicts, Stow: ' + ', '.join(PACKAGES))
            print('Would enable gh completion in Bash and existing Zsh startup files.')
            print('Would enable nvim-server and yazi-nvim shell aliases.')
            print('Would restore locked Neovim plugins' if not self.args.skip_plugins else 'Plugin restore skipped')
            return
        self.bin.mkdir(parents=True, exist_ok=True)
        os.environ['PATH'] = str(self.bin) + os.pathsep + os.environ.get('PATH', '')
        if not self.args.configs_only:
            # Install preserves existing tools. Update resolves current stable releases.
            if self.args.update or not shutil.which('nvim'):
                nvarch = 'arm64' if arch == 'aarch64' else arch
                self.release('nvim', 'neovim/neovim', f'nvim-linux-{nvarch}.tar.gz', {'nvim': 'bin/nvim'})
            if self.args.update or not all(shutil.which(x) for x in ('yazi', 'ya')):
                self.release('yazi', 'sxyazi/yazi', f'yazi-{arch}-unknown-linux-musl.zip', {'yazi': 'yazi', 'ya': 'ya'})
            if self.args.update or not shutil.which('zellij'):
                self.release('zellij', 'zellij-org/zellij', f'zellij-{arch}-unknown-linux-musl.tar.gz', {'zellij': 'zellij'})
            if self.args.update or not shutil.which('lazygit'):
                lgarch = 'arm64' if arch == 'aarch64' else arch
                self.release('lazygit', 'jesseduffield/lazygit', f'lazygit_{{version}}_linux_{lgarch}.tar.gz', {'lazygit': 'lazygit'})
            if self.args.update or not shutil.which('gh'):
                gharch = 'amd64' if arch == 'x86_64' else 'arm64'
                self.release('gh', 'cli/cli', f'gh_{{version}}_linux_{gharch}.tar.gz', {'gh': 'bin/gh'})
            if self.args.update or not shutil.which('codex'):
                target = f'codex-{arch}-unknown-linux-musl'
                self.release('codex', 'openai/codex', f'{target}.tar.gz', {'codex': target})
            if self.args.update or not shutil.which('claude'):
                self.claude()
            if self.args.update or not shutil.which('stow'):
                self.stow()
        self.configs()
        for rc in (self.home / '.bashrc', self.home / '.zshrc'):
            if rc.name == '.bashrc' or rc.exists():
                line = '\n# Dotfiles: user-local tools\nexport PATH="$HOME/.local/bin:$PATH"\n'
                content = rc.read_text() if rc.exists() else ''
                if '# Dotfiles: user-local tools' not in content and '"$HOME/.local/bin:$PATH"' not in content:
                    backup = self.backups / rc.relative_to(self.home)
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    if rc.exists():
                        shutil.copy2(rc, backup)
                    with rc.open('a') as stream:
                        stream.write(line)
                shell = 'bash' if rc.name == '.bashrc' else 'zsh'
                marker = '# Dotfiles: gh completion'
                content = rc.read_text() if rc.exists() else ''
                if marker not in content:
                    backup = self.backups / rc.relative_to(self.home)
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    if rc.exists() and not backup.exists():
                        shutil.copy2(rc, backup)
                    with rc.open('a') as stream:
                        stream.write(f'\n{marker}\n[ ! -r "$HOME/.config/shell/gh-completion.{shell}" ] || . "$HOME/.config/shell/gh-completion.{shell}"\n')
                marker = '# Dotfiles: shared Neovim/Yazi aliases'
                content = rc.read_text() if rc.exists() else ''
                if marker not in content:
                    backup = self.backups / rc.relative_to(self.home)
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    if rc.exists() and not backup.exists():
                        shutil.copy2(rc, backup)
                    with rc.open('a') as stream:
                        stream.write(f'\n{marker}\n[ ! -r "$HOME/.config/shell/editor-aliases.sh" ] || . "$HOME/.config/shell/editor-aliases.sh"\n')
        if not self.args.skip_plugins:
            run('nvim', '--headless', '+Lazy! restore', '+qa')
        print('Setup complete. Open a new shell, or run: export PATH="$HOME/.local/bin:$PATH"')
        if self.backups.exists():
            print(f'Backups: {self.backups}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--update', action='store_true', help='update tools to latest stable releases')
    parser.add_argument('--no-pull', action='store_true', help='update.sh: skip Git pull')
    parser.add_argument('--configs-only', action='store_true', help='apply configs using installed Stow')
    parser.add_argument('--skip-plugins', action='store_true', help='skip restoring locked Neovim plugins')
    parser.add_argument('--dry-run', action='store_true', help='print plan without network or filesystem changes')
    args = parser.parse_args()
    try:
        Setup(args).main()
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f'Setup failed: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
