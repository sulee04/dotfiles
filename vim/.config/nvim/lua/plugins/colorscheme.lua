return {
  {
    "gbprod/nord.nvim",
    lazy = false,
    priority = 1000,
    opts = {
      transparent = true,
      on_highlights = function(highlights, colors)
        -- Opaque popup surfaces stand out from the terminal background.
        highlights.NormalFloat = { fg = colors.snow_storm.brightest, bg = colors.polar_night.bright }
        highlights.FloatBorder = { fg = colors.frost.ice, bg = colors.polar_night.bright }
        highlights.FloatTitle = { fg = colors.frost.ice, bg = colors.polar_night.bright, bold = true }
      end,
    },
    config = function(_, opts)
      require("nord").setup(opts)
      vim.cmd.colorscheme("nord")
    end,
  },
}
