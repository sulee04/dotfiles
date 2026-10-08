return {
  {
    "lewis6991/gitsigns.nvim",
    event = { "BufReadPre", "BufNewFile" },
    keys = {
      { "<leader>gp", function() require("gitsigns").preview_hunk() end, desc = "Preview hunk" },
      { "<leader>gs", function() require("gitsigns").stage_hunk() end, desc = "Stage/unstage hunk" },
      { "<leader>gr", function()
        vim.ui.select({ "Cancel", "Reset hunk" }, { prompt = "Discard this hunk's buffer edits?" }, function(choice)
          if choice == "Reset hunk" then require("gitsigns").reset_hunk() end
        end)
      end, desc = "Reset hunk (confirm)" },
      { "<leader>gb", function() require("gitsigns").blame_line({ full = true }) end, desc = "Blame current line" },
    },
    opts = {
      signs = {
        add = { text = "+" },
        change = { text = "~" },
        delete = { text = "_" },
        topdelete = { text = "-" },
        changedelete = { text = "~" },
        untracked = { text = "?" },
      },
      signs_staged = {
        add = { text = "+" },
        change = { text = "~" },
        delete = { text = "_" },
        topdelete = { text = "-" },
        changedelete = { text = "~" },
        untracked = { text = "?" },
      },
      attach_to_untracked = true,
      current_line_blame = false,
      preview_config = { border = "rounded" },
      on_attach = function(buf)
        local gs = require("gitsigns")
        local function map(lhs, rhs, desc)
          vim.keymap.set("n", lhs, rhs, { buffer = buf, desc = desc })
        end
        map("]c", function() gs.nav_hunk("next") end, "Next Git hunk")
        map("[c", function() gs.nav_hunk("prev") end, "Previous Git hunk")
      end,
    },
  },
}
