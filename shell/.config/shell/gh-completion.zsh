# Initialize Zsh completion only if the user's shell has not already done so.
if command -v gh >/dev/null 2>&1; then
  if (( ! $+functions[compdef] )); then
    autoload -Uz compinit
    compinit
  fi
  source <(gh completion --shell zsh)
fi
