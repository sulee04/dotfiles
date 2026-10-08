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
