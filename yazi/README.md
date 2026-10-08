# Yazi appearance

`theme.toml` uses Nord colors, square hovered-file indicators, and flat tab/status
separators. Icons retain their Nerd Fonts glyphs and use Nord4 (`#D8DEE9`) for a
neutral, monochrome appearance. Their colors are set by Yazi, not the font.

Icon rules are copied from Yazi 26.9.1's default theme and only their foreground
colors are changed. This preserves file-type shapes and matching rules. Future
Yazi updates retain this snapshot rather than introducing new colored defaults.

Restart Yazi to reload the theme. Stow deploys it with the `yazi` package.
The `yazi.toml` and editor-helper links use the integration in the `vim` package.

References: https://yazi-rs.github.io/docs/configuration/theme/
and https://yazi-rs.github.io/docs/faq/#i-dont-like-nerd-fonts

## Git workflow

Git status appears at the right edge of file rows and propagates to folders.
Markers: `?` untracked, `M` modified, `S` staged, `A` added, `D` deleted,
`U` unmerged/updated, `!` ignored. Colors use Nord; file icons stay monochrome.

Press **g, then i** inside a repository to open Lazygit for that repository.
Press **q** in Lazygit to return to Yazi. Outside a repository, the launcher
shows a message and returns after Enter without creating a repository.
Lazygit uses square borders and a Nord palette. Git actions such as staging,
committing, and pushing happen only when you choose them in Lazygit.

The official `git.yazi` plugin is bundled at the commit in its `UPSTREAM` file,
including its MIT license. Stow installs it with no extra plugin download.
Plugin updates come through dotfile commits; the installer updates Lazygit to
its stable release when you run `update.sh`.

Source: https://github.com/yazi-rs/plugins/tree/main/git.yazi

From Yazi's blocking shell (`:`), run `yazi-lazygit` instead of bare `lazygit`.
The launcher verifies the current directory belongs to a repository and passes
its root explicitly, so a non-repository directory cannot reopen a recent repo.
Lazygit normally displays the whole repository, even when launched from a subfolder.
