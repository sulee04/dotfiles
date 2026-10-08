# Neovim configuration

Personal Lua configuration using lazy.nvim, built one feature at a time.

## Files

- `init.lua`: loads settings, keybindings, and the plugin manager.
- `lua/config/options.lua`: editor settings.
- `lua/config/keymaps.lua`: keybindings; Space is the leader and backslash is the local leader.
- `lua/config/lazy.lua`: bootstraps and configures lazy.nvim.
- `lua/plugins/`: plugin specifications.
- `lazy-lock.json`: plugin revisions; commit changes when intentionally updating plugins.

Plugins are installed under Neovim's data directory, outside this repository.
First startup requires Git and access to GitHub.

## Commands

- `:Lazy`: open the plugin manager.
- `:Lazy sync`: install missing plugins and update configured plugins.
- `:Lazy restore`: restore plugin revisions recorded in the lockfile.
- `:checkhealth lazy`: check plugin-manager health.

Automatic update checks are disabled; updates are performed manually.
LuaRocks support is disabled because no configured plugins require it.

## Editor behavior

Relative line numbers, two-space indentation, smart-case search, persistent undo,
an eight-line scroll margin, cursor-line highlighting, and a fixed sign column
are enabled. Long lines do not wrap. Press Escape in normal mode to clear search
highlighting. Pane navigation is handled by Zellij; no split mappings are added.

On `FocusGained` and `BufEnter`, Neovim checks for external file changes.
Unmodified buffers reload automatically; unsaved edits are protected by Neovim's
normal conflict handling. This reloads file contents, not Lua configuration.
Focus detection depends on the terminal and Zellij delivering focus events;
`:checktime` performs the same check manually.

System clipboard sharing is enabled only when Neovim detects a provider.
No provider was available in the setup environment.

## Colors

Nord is loaded at startup using `gbprod/nord.nvim`, with true colors enabled.
The main background is transparent so it uses the terminal's Nord background.
To use the theme's own background, set `transparent = false` in
`lua/plugins/colorscheme.lua` and restart Neovim.

## Finding files and text

Telescope loads when a search shortcut or `:Telescope` is used.

| Shortcut (normal mode) | Action |
| --- | --- |
| Space f f | Find files |
| Space f g | Search project text (regular expressions) |
| Space f b | Switch open buffers |
| Space f h | Search Neovim and plugin help |

Search starts in Neovim's current working directory (`:pwd`). Open Neovim from
the project directory, or use `:cd /path/to/project` to change the search scope.
File and text searches include hidden files, respect ignore files, and exclude
`.git`. Ripgrep (`rg`) must be available on PATH; it is available in this setup.

Type to filter results, use Ctrl-n/Ctrl-p or arrow keys to select, and press
Enter to open the result in the current window. Escape enters normal mode in
the picker; press Escape again to close it. Split and tab-opening shortcuts
are disabled because Zellij handles panes.

## Syntax highlighting

Tree-sitter highlighting is enabled for OCaml (`.ml` and `.mli`), Python, Rust,
JavaScript/JSX, HTML, and CSS. Parsers install automatically when missing.
The Tree-sitter CLI lives in `~/.local/bin/tree-sitter`; parser builds also need
a C compiler, curl, and tar. Run `:TSUpdate` after plugin updates. If opening a
file during the initial install, reopen it after installation completes.

Lean's experimental Tree-sitter parser is not enabled. lean.nvim provides
Lean syntax highlighting and language-server semantic tokens.
This step does not change indentation, folds, or editing shortcuts.

## Language servers

Lean, OCaml, Python, and Rust have language-server support. JavaScript, HTML,
and CSS currently have syntax highlighting only.

| Language | Server and environment |
| --- | --- |
| Lean | lean.nvim uses the project's elan toolchain and Lake environment |
| OCaml | `opam exec -- ocamllsp` runs from the project root, selecting its switch |
| Python | BasedPyright, installed with `uv tool install basedpyright` |
| Rust | rust-analyzer, installed through rustup with rust-src |

Python's server runs in its own isolated tool environment. Open Neovim from
your activated project environment or use a project `.venv` for dependency
resolution. To select an interpreter explicitly, run
`:LspPyrightSetPythonPath /path/to/venv/bin/python` in a Python buffer.
Build OCaml projects with Dune so their editor metadata exists.
Rust analysis needs Cargo and the standard-library sources for the project's
toolchain (`rustup component add rust-src` if using another toolchain).
Lean projects use their `lean-toolchain` file, not a hard-coded Lean version.

The setup installed BasedPyright 1.40.2 (with its bundled Node runtime) and
Rust stable 1.99.0 with rust-analyzer and rust-src. uv and server launchers are
available in `~/.local/bin`; Rust itself is managed under `~/.cargo` and
`~/.rustup`. Existing OCaml and elan installations are reused. No automatic
formatting or completion popup is enabled in this step.

| Shortcut | Action |
| --- | --- |
| `gd` | Go to definition; Telescope handles multiple results |
| `K` | Hover documentation |
| `Space c r` | Rename symbol |
| `Space c a` | Code action |
| `Space c R` | Find references in Telescope |
| `Space d d` | Show diagnostics for the current line |
| `Space d l` | List current-buffer diagnostics in Telescope |
| `[d` / `]d` | Previous / next diagnostic (Neovim built-in) |
| `Space l g` | Lean goal in a floating popup |
| `Space l r` | Restart the current Lean file |

Shortcuts are added when a server attaches to the buffer. which-key groups them
under Code, Diagnostics, and Lean. Errors are underlined and marked E/W/I/H in
the sign column; diagnostic text appears when requested rather than beside
every line. Lean's infoview does not open automatically; `:LeanInfoviewToggle`
can open it explicitly in a separate tab. Lean server stderr panes are disabled;
use `:LspLog` to investigate server problems. `:checkhealth vim.lsp` lists the
enabled servers, and `:LspInfo` reports clients for the current session.

## Shortcut hints

Press Space and pause for 300 ms to see available shortcuts through which-key.
Press f to expand the Find group, then f/g/b/h to launch the corresponding
Telescope search. Escape dismisses the hints. Mapping icons are disabled and
common key labels use plain text. Existing shortcuts are unchanged.

## File browsing

Run `yazi` from a terminal or `:terminal yazi` inside Neovim. Its editor opener
uses the surrounding Neovim when `$NVIM` is set, and starts Neovim otherwise.
See [the Yazi integration guide](integrations/yazi/README.md) for usage,
bulk-renaming instructions, and deployment details.
