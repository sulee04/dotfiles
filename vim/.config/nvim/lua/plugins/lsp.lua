return {
  {
    "neovim/nvim-lspconfig",
    lazy = false,
    config = function()
      require("config.lsp")
    end,
  },
  {
    "Julian/lean.nvim",
    event = { "BufReadPre *.lean", "BufNewFile *.lean" },
    init = function()
      -- Set before lean.nvim's plugin files initialize its language server.
      vim.g.lean_config = {
        mappings = false,
        infoview = { autoopen = false, separate_tab = true },
        stderr = { enable = false },
        graphics = { enabled = false },
      }
    end,
  },
}
