# Neovim configuration checklist

Build a personal Lua configuration using lazy.nvim. Work through one item at a time, explain the settings and keybindings, verify the result, and then mark it complete. Choose plugins when we reach each feature, based on the installed Neovim version and your preferences.

## Foundation

- [x] 1. **lazy.nvim and configuration structure** — Check Neovim and Git versions, preserve any existing configuration, bootstrap lazy.nvim, and split options, keymaps, and plugins into small Lua files. Verify startup and `:checkhealth lazy`; keep `lazy-lock.json` for reproducible plugin versions.
- [x] 2. **Essential editor settings** — Relative line numbers, two-space indentation, smart-case search, clipboard integration where supported, persistent undo, scrolling and display settings, and Escape to clear search highlights. Use Zellij for panes; no split settings or shortcuts. Check external file changes on focus regain and buffer entry; reload unmodified buffers automatically.
- [x] 3. **Colors and readability** — Nord (`gbprod/nord.nvim`) loads at startup with true colors and a transparent main background to match Nord in iTerm2 and Zellij. Startup and highlight settings verified. Icons remain optional for later features.

## Everyday navigation

- [x] 4. **Fuzzy finding and project search** — Telescope with ripgrep: Space f f finds files, Space f g searches project text, Space f b switches buffers, and Space f h searches help. Hidden files included, ignore files respected, `.git` excluded. Searches start in `:pwd`. Split and tab-opening shortcuts disabled; all four pickers smoke-tested. Health check passes required dependencies; optional fd is absent.
- [x] 5. **File browsing** — Standalone Yazi 26.9.1 and `ya` installed in `~/.local/bin`. `yazi` works in ordinary terminals; `:terminal yazi` reuses the parent Neovim through `$NVIM`. Hidden files visible; Nord terminal palette inherited. Version-controlled config and editor wrapper live in `~/.config/nvim/integrations/yazi`, symlinked to their active locations. Bulk renaming waits for `:w` then `:bd` in the parent editor. Ordinary and remote opening, special filenames, multiple buffers, unsaved-edit retention, bulk waiting, and TUI startup verified.
- [x] 6. **Discoverable keybindings** — which-key.nvim shows hints after a 300 ms pause. Space f opens the Find group with all four Telescope shortcuts. Icons disabled and key labels use plain text. Interactive popup verified; no mapping conflicts or duplicates.

## Coding essentials

- [x] 7. **Syntax highlighting with Tree-sitter** — Installed and verified OCaml implementation/interface, Python, Rust, JavaScript/JSX, HTML, and CSS parsers. Tree-sitter CLI 0.27.1 installed in `~/.local/bin`. Lean's experimental parser is excluded; Lean highlighting will be configured through lean.nvim in item 8. No folding or indentation changes.
- [x] 8. **Language servers and diagnostics** — Lean (`lean.nvim`/elan), OCaml (`opam exec -- ocamllsp`), Python (BasedPyright), and Rust (rust-analyzer). Installed user-local Python server and minimal Rust toolchain with rust-src. All four attached and emitted errors in isolated projects; shortcuts verified and no automatic splits. Code/Diagnostics/Lean groups in which-key; Telescope handles result lists; Lean goal popup with Space l g. Lean syntax highlighting enabled. JavaScript/HTML/CSS servers deferred by request.
- [ ] 9. **Completion and snippets (deferred)** — Add completion for language-server suggestions, paths, and useful snippets, with explicit accept and navigation keys. Deferred by preference: add this when the need becomes apparent.
- [ ] 10. **Formatting** — Choose formatters per language and add a manual format shortcut. Decide whether formatting on save suits your workflow; avoid competing formatters.
- [ ] 11. **Linting, where needed** — Add checks that your language servers do not already provide, and display results through Neovim diagnostics.
- [ ] 12. **Editing helpers** — Convenient commenting, paired brackets and quotes, and changing surrounding quotes or brackets. Use built-in features where they already meet the need.

## Workflow and polish

- [x] 13. **Git integration** — gitsigns.nvim adds change markers and a Git group in which-key. `]c`/`[c` navigate hunks; Space g p previews, Space g s stages/unstages, Space g r resets with confirmation, and Space g b shows line blame. Tested detection, floating preview, stage/unstage, reset, and shortcut attachment in a temporary repository. Lazygit will be managed by you.
- [ ] 14. **Statusline** — Show the current file, modified state, Git branch, diagnostics, and cursor position without excessive clutter.
- [ ] 15. **Terminal and task shortcuts (optional)** — Open a terminal and run common build or test commands for your projects.
- [ ] 16. **Sessions (optional)** — Restore useful windows and buffers when returning to a project; choose when sessions should be saved or loaded.
- [ ] 17. **Debugging (optional)** — Add debugger integration only for languages and projects where you need it.
- [ ] 18. **Maintenance and final check** — Run relevant health checks, document keybindings, keep the configuration under version control, and learn how to update or restore plugin versions.

## Current progress

Items 1–8 and 13 completed. Configuration lives in `~/dotfiles/vim/.config/nvim`, linked from `~/.config/nvim`. Space is the leader; backslash is the local leader. Essential editor settings and external-file reload checks enabled; Zellij handles panes. No clipboard provider detected, so system clipboard sharing remains conditional. Nord enabled with true colors and a transparent main background. Telescope configured for files, project text, buffers, and help. Standalone Yazi reuses the parent editor in new tabs, using a headless remote client. which-key shows shortcut hints. Tree-sitter highlighting enabled for OCaml, Python, Rust, and web files; lean.nvim supplies Lean syntax and semantic highlighting. Language servers enabled for Lean, OCaml, Python, and Rust. Git actions under Space g are global; LSP actions attach per buffer.

Git integration (item 13) was completed ahead of completion by request. Completion and snippets are deferred until you miss them; remaining unchecked features are available to revisit as needed. This checklist is version-controlled in the dotfiles repository.

## References

- [lazy.nvim installation](https://lazy.folke.io/installation)
- [lazy.nvim plugin manager and lockfile](https://github.com/folke/lazy.nvim)
- [Neovim language-server documentation](https://neovim.io/doc/user/lsp)
- [Neovim Tree-sitter documentation](https://neovim.io/doc/user/treesitter/)
- [Neovim health checks](https://neovim.io/doc/user/health/)
