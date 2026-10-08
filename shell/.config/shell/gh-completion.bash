# Load completions from the installed gh, so tool updates need no regeneration.
if command -v gh >/dev/null 2>&1; then
  if ! declare -F _get_comp_words_by_ref >/dev/null 2>&1; then
    if [[ -r /usr/share/bash-completion/bash_completion ]]; then
      . /usr/share/bash-completion/bash_completion
    elif [[ -r /etc/bash_completion ]]; then
      . /etc/bash_completion
    fi
  fi
  eval "$(gh completion --shell bash)"
fi
