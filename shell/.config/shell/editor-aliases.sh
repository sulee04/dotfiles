# Remove aliases when re-sourcing this file in an existing shell.
unalias nvim-server yazi-nvim 2>/dev/null || :

_nvim_folder_socket() {
    local folder_path folder_key folder_hash
    folder_path=$(pwd -P) || return
    # Encode separators, spaces and shell metacharacters as underscores. Keep
    # the name short for Unix socket limits; the checksum identifies the full path.
    folder_key=$(printf '%s' "$folder_path" | LC_ALL=C tr -c 'A-Za-z0-9._-' '_' | cut -c 1-24)
    folder_hash=$(printf '%s' "$folder_path" | cksum)
    folder_hash=${folder_hash%% *}
    printf '/tmp/nvim-%s/%s-%s.sock\n' "$(id -u)" "$folder_key" "$folder_hash"
}

nvim-server() {
    local socket_path
    socket_path=$(_nvim_folder_socket) || return
    mkdir -p -m 700 "${socket_path%/*}" || return
    printf 'Neovim socket: %s\n' "$socket_path"
    NVIM="$socket_path" command nvim --listen "$socket_path" "$@"
}

yazi-nvim() {
    local socket_path
    socket_path=$(_nvim_folder_socket) || return
    NVIM="$socket_path" command yazi "$@"
}
