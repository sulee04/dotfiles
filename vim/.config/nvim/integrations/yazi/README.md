# Yazi integration

Yazi 26.9.1 and `ya` are installed in `~/.local/bin`. The editor wrapper and
configuration are tracked here and symlinked into `~/.local/bin/nvim-yazi-editor`
and `~/.config/yazi/yazi.toml`. Python 3 and Neovim must be on PATH.

Run `yazi` in any terminal, or `:terminal yazi` inside Neovim, then press `i`
to interact if needed. Use h/j/k/l to navigate, Enter to open a file, Space to
select, r to rename, and q to quit. Use `~` for Yazi's help.

Ordinary terminals launch Neovim and return to Yazi after the editor exits.
Inside Neovim, `$NVIM` identifies the surrounding instance: the wrapper opens
each selected file in a new tab and exits terminal mode. No nested editor or
split is created. Yazi continues in its original tab; use `gt` / `gT` to switch
tabs and i to resume interacting with its terminal. Unsaved buffers are retained.
Without `$NVIM`, a new Neovim instance opens with one tab per selected file.

Bulk rename uses the same editor but waits for the rename-list buffer to be
unloaded. In the parent Neovim, edit the list, run `:w`, then `:bd` to finish;
return to Yazi's terminal buffer to review and confirm the operation. In an
ordinary terminal, use `:wq`. Do not exit the entire parent Neovim to finish
a rename. If the parent server cannot be reached, the wrapper reports an error.

Yazi uses the terminal palette by default, so it inherits your Nord terminal
colors. Advanced image, PDF, and video previews may need optional external
tools; those are not installed by this setup.

To deploy the tracked configuration on another machine:

```sh
mkdir -p ~/.local/bin ~/.config/yazi
chmod +x ~/.config/nvim/integrations/yazi/nvim-yazi-editor
ln -s ~/.config/nvim/integrations/yazi/nvim-yazi-editor ~/.local/bin/nvim-yazi-editor
ln -s ~/.config/nvim/integrations/yazi/yazi.toml ~/.config/yazi/yazi.toml
```

Install Yazi for that machine's operating system separately. Do not replace
an existing Yazi configuration without reviewing it first.
