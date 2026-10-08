# Personal dotfiles

Linux x86-64 and ARM64 setup for Neovim, Yazi (`yazi` and `ya`), Zellij, Lazygit, and GNU Stow. Stow manages your Neovim, Yazi, Zellij, and Codex settings.

## Set up a machine

```sh
git clone <your-dotfiles-repository-url> ~/dotfiles
cd ~/dotfiles
./install.sh
```

Open a new shell afterward. The script works from any directory; you can clone somewhere other than `~/dotfiles`.

Requires Python 3.9+, Git, Perl, make, tar, unzip, ripgrep, and CA certificates. Missing prerequisites are installed automatically through apt/sudo on Debian and Ubuntu (sudo may request your password). Other Linux distributions need these prerequisites installed first. Git is needed to clone. Neovim's official binary also needs a compatible glibc; Ubuntu 24.04 is suitable.

Missing tools are downloaded from official stable releases into `~/.local/opt/dotfiles` and linked from `~/.local/bin`. Stow is built from its official source release. Existing installed tools are retained by `install.sh`. GitHub asset SHA-256 digests are verified when provided; downloads use HTTPS. Internet access is needed for downloads and plugin restoration.

Conflicting config files, directories, and symlinks are backed up under `~/.local/share/dotfiles-backups/<timestamp>/`. Unrelated config files stay in place. A config parent directory linking outside this repository must be relocated before setup. Repeating setup is safe. Bash and an existing Zsh configuration gain `~/.local/bin` on PATH, with backups before editing.

Neovim plugins are restored using the tracked `lazy-lock.json`. Codex's config is included, but its application is installed separately. Credentials, sessions, databases, caches, and editor data are excluded. Optional preview tools, clipboard providers, fonts, language servers, and terminal colors are configured separately.

## Update

```sh
./update.sh                     # fast-forward Git, update stable tools, restore plugins
./update.sh --no-pull           # use this checkout without pulling
```

Pulling requires a clean checkout and uses `git pull --ff-only`. Without an upstream, the script updates tools and applies local configs. Binary launchers are backed up before replacement; older version directories remain available.

Plugins remain pinned to the lockfile. To deliberately upgrade plugins, run `:Lazy update` in Neovim and commit the changed lockfile.

```sh
./install.sh --dry-run                        # plan without downloads or changes
./install.sh --configs-only --skip-plugins    # configs only, requires Stow
./install.sh --skip-plugins                   # skip restoring plugins
./update.sh --dry-run                         # preview without Git pull
```

## Stow packages

| Package | Home paths |
| --- | --- |
| `vim` | `.config/nvim/` (Neovim, rather than traditional Vim) |
| `yazi` | `.config/yazi/yazi.toml`, `.local/bin/nvim-yazi-editor` |
| `zellij` | `.config/zellij/config.kdl` |
| `codex` | `.codex/config.toml` |
| `lazygit` | `.config/lazygit/config.yml` |

Yazi's package uses relative links to the integration files in the Neovim package, keeping one source that survives cloning.

```sh
cd ~/dotfiles
stow --target="$HOME" --simulate --restow vim yazi zellij codex lazygit
stow --target="$HOME" --restow vim yazi zellij codex lazygit
stow --target="$HOME" --delete vim yazi zellij codex lazygit
```

Deleting links retains repository files. To restore an original config, remove its Stow link and move the corresponding backup to its original path. `.stowrc` defaults to the repository's parent; scripts always pass the home target explicitly.

## Repository

This is one Git repository. Neovim's previous Git history was preserved at `~/.local/share/dotfiles-backups/20261008T183339Z/nvim-git-history`. Its config files, lockfile, and uncommitted work are included here. No remote has been created or published. Create a repository on your Git host, then:

```sh
git remote add origin <your-dotfiles-repository-url>
git push -u origin main
```

## Checks and sources

```sh
python3 -m unittest discover -s tests -v
bash -n install.sh update.sh
```

Official sources: [Neovim installation](https://github.com/neovim/neovim/blob/master/INSTALL.md), [Yazi releases](https://github.com/sxyazi/yazi/releases), [Zellij releases](https://github.com/zellij-org/zellij/releases), [GNU Stow](https://www.gnu.org/software/stow/).

Yazi includes Git status indicators and **g, then i** to open Lazygit; **q** returns
to Yazi. Both use Nord. The Git plugin is bundled at a fixed revision. See
[yazi/README.md](yazi/README.md) for markers and controls.
