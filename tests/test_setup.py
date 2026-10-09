import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

spec = importlib.util.spec_from_file_location('setup', Path(__file__).resolve().parents[1] / 'scripts/setup.py')
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


@unittest.skipUnless(shutil.which('stow'), 'GNU Stow required')
class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / 'home'
        self.home.mkdir()
        self.repo = Path(self.temp.name) / 'checkout'
        shutil.copytree(setup.REPO, self.repo, symlinks=True,
                        ignore=shutil.ignore_patterns('.git', '__pycache__'))
        env = patch.object(Path, 'home', return_value=self.home)
        env.start()
        self.addCleanup(env.stop)
        repo_patch = patch.object(setup, 'REPO', self.repo)
        repo_patch.start()
        self.addCleanup(repo_patch.stop)
        self.instance = setup.Setup(SimpleNamespace())

    def test_fresh_checkout_and_repeat(self):
        self.instance.configs()
        config = self.home / '.config/yazi/yazi.toml'
        helper = self.home / '.local/bin/nvim-yazi-editor'
        self.assertEqual(config.resolve(), self.repo / 'vim/.config/nvim/integrations/yazi/yazi.toml')
        self.assertTrue(os.access(helper, os.X_OK))
        self.assertTrue((self.home / '.config/nvim/README.md').exists())
        self.instance.configs()
        self.assertFalse(self.instance.backups.exists())

    def test_conflicts_are_backed_up(self):
        config = self.home / '.config/zellij/config.kdl'
        config.parent.mkdir(parents=True)
        config.write_text('old config')
        unrelated = config.parent / 'other.kdl'
        unrelated.write_text('keep me')
        self.instance.configs()
        self.assertEqual((self.instance.backups / '.config/zellij/config.kdl').read_text(), 'old config')
        self.assertEqual(unrelated.read_text(), 'keep me')

    def test_absolute_links_are_replaced(self):
        config = self.home / '.config/yazi/yazi.toml'
        config.parent.mkdir(parents=True)
        config.symlink_to(self.repo / 'vim/.config/nvim/integrations/yazi/yazi.toml')
        self.instance.configs()
        self.assertFalse(os.path.isabs(os.readlink(config)))
        self.assertTrue((self.instance.backups / '.config/yazi/yazi.toml').is_symlink())

    def test_existing_folded_directory_preserves_source_links(self):
        target = self.home / '.config/yazi'
        target.parent.mkdir()
        target.symlink_to(os.path.relpath(self.repo / 'yazi/.config/yazi', target.parent))
        self.instance.configs()
        self.assertTrue((self.repo / 'yazi/.config/yazi/yazi.toml').is_symlink())
        self.assertTrue((target / 'yazi.toml').is_file())

    def test_failure_restores_original_config(self):
        config = self.home / '.codex/config.toml'
        config.parent.mkdir()
        config.write_text('original')
        with patch.object(setup, 'run', side_effect=subprocess.CalledProcessError(1, 'stow')):
            with self.assertRaises(subprocess.CalledProcessError):
                self.instance.configs()
        self.assertEqual(config.read_text(), 'original')

    def test_external_parent_symlink_is_untouched(self):
        other = Path(self.temp.name) / 'external'
        other.mkdir()
        (self.home / '.config').symlink_to(other)
        with self.assertRaisesRegex(RuntimeError, 'links outside'):
            self.instance.configs()
        self.assertEqual(list(other.iterdir()), [])
        self.assertTrue((self.home / '.config').is_symlink())


class AgentInstallTests(unittest.TestCase):
    def test_install_modes(self):
        cases = (
            ('existing', False, False, False, False, False),
            ('missing', True, False, False, False, True),
            ('update', False, True, False, False, True),
            ('configs_only', True, True, True, False, False),
            ('dry_run', True, True, False, True, False),
        )
        for arch in ('x86_64', 'aarch64'):
            for name, missing, update, configs_only, dry_run, install in cases:
                with self.subTest(arch=arch, mode=name), tempfile.TemporaryDirectory() as temp:
                    args = SimpleNamespace(update=update, configs_only=configs_only,
                                           dry_run=dry_run, skip_plugins=True)
                    def which(command):
                        return None if missing and command in ('codex', 'claude') else f'/usr/bin/{command}'
                    with patch.object(Path, 'home', return_value=Path(temp)), \
                            patch.object(setup.platform, 'system', return_value='Linux'), \
                            patch.object(setup.platform, 'machine', return_value=arch), \
                            patch.object(setup.shutil, 'which', side_effect=which), \
                            patch.dict(os.environ), \
                            patch.object(setup.Setup, 'release') as release, \
                            patch.object(setup.Setup, 'claude') as claude, \
                            patch.object(setup.Setup, 'stow'), \
                            patch.object(setup.Setup, 'configs'), \
                            patch.object(setup, 'fetch') as fetch:
                        setup.Setup(args).main()
                        codex_calls = [call for call in release.call_args_list if call.args[0] == 'codex']
                        self.assertEqual(len(codex_calls), int(install))
                        self.assertEqual(claude.call_count, int(install))
                        if install:
                            target = f'codex-{arch}-unknown-linux-musl'
                            self.assertEqual(codex_calls[0].args,
                                             ('codex', 'openai/codex', f'{target}.tar.gz', {'codex': target}))
                        fetch.assert_not_called()
                        if dry_run:
                            self.assertEqual(list(Path(temp).iterdir()), [])

    def test_claude_installer_and_verification(self):
        with tempfile.TemporaryDirectory() as temp, \
                patch.object(Path, 'home', return_value=Path(temp)), \
                patch.object(setup.shutil, 'which', return_value='/usr/bin/curl'), \
                patch.object(setup, 'fetch') as fetch, patch.object(setup, 'run') as run:
            instance = setup.Setup(SimpleNamespace())
            instance.claude()
            installer = fetch.call_args.args[1]
            self.assertEqual(fetch.call_args.args[0], 'https://claude.ai/install.sh')
            self.assertEqual(run.call_args_list[0].args, ('bash', installer, 'stable'))
            self.assertEqual(run.call_args_list[1].args, (instance.bin / 'claude', '--version'))
            self.assertFalse(installer.exists())

    def test_claude_requires_downloader(self):
        with patch.object(setup.shutil, 'which', return_value=None), \
                patch.object(setup, 'fetch') as fetch:
            with self.assertRaisesRegex(RuntimeError, 'curl or wget'):
                setup.Setup(SimpleNamespace()).claude()
            fetch.assert_not_called()

    def test_claude_install_failure_propagates(self):
        with patch.object(setup.shutil, 'which', return_value='/usr/bin/curl'), \
                patch.object(setup, 'fetch'), \
                patch.object(setup, 'run', side_effect=subprocess.CalledProcessError(1, 'bash')):
            with self.assertRaises(subprocess.CalledProcessError):
                setup.Setup(SimpleNamespace()).claude()
