# Start the shared editor first, then launch Yazi from another terminal/pane.
alias nvim-server='mkdir -p "$HOME/.cache/nvim" && nvim --listen "$HOME/.cache/nvim/editor.sock"'
alias yazi-nvim='NVIM="$HOME/.cache/nvim/editor.sock" yazi'
