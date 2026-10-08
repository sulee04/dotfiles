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
