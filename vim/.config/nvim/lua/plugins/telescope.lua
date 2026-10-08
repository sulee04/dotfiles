return {
  {
    "nvim-telescope/telescope.nvim",
    version = "*",
    cmd = "Telescope",
    dependencies = { "nvim-lua/plenary.nvim" },
    keys = {
      { "<leader>ff", "<cmd>Telescope find_files<CR>", desc = "Find files" },
      { "<leader>fg", "<cmd>Telescope live_grep<CR>", desc = "Search project text" },
      { "<leader>fb", "<cmd>Telescope buffers<CR>", desc = "Find open buffers" },
      { "<leader>fh", "<cmd>Telescope help_tags<CR>", desc = "Search help" },
    },
    opts = {
      defaults = {
        -- Open results in the current window; Zellij handles panes.
        mappings = {
          i = { ["<C-x>"] = false, ["<C-v>"] = false, ["<C-t>"] = false },
          n = { ["<C-x>"] = false, ["<C-v>"] = false, ["<C-t>"] = false },
        },
      },
      pickers = {
        find_files = {
          find_command = { "rg", "--files", "--hidden", "--glob", "!.git" },
        },
        live_grep = {
          additional_args = { "--hidden", "--glob", "!.git" },
        },
      },
    },
  },
}
