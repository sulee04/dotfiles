# Nord colors in Codex CLI

`tui.theme = "nord-muted"` loads `.codex/themes/nord-muted.tmTheme` through Stow.
The custom theme uses Nord colors for syntax and markup. Added diff lines use
Nord1 (`#3B4252`) backgrounds; removed lines use Nord2 (`#434C5E`), replacing
Codex's default red/green fills. Scoped addition/deletion foregrounds are Nord
Aurora green (`#A3BE8C`) and red (`#BF616A`).

Codex 0.161.0 supports these TextMate scope background overrides. Its diff
signs and unhighlighted text still use ANSI green/red; other interface elements
also use terminal ANSI colors. Those colors come from your terminal profile.

Your iTerm2 profile already uses Nord, so no terminal palette change is needed.

Restart Codex, or run `/theme` and select `nord-muted`, to load the custom theme.
Truecolor terminals show exact colors; 256-color terminals approximate them.
