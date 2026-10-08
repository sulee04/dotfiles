return {
  {
    "nvim-treesitter/nvim-treesitter",
    branch = "main",
    lazy = false,
    build = ":TSUpdate",
    config = function()
      local ts = require("nvim-treesitter")
      ts.setup({})
      -- Missing parsers install asynchronously; use :TSInstall to retry.
      ts.install({
        "ocaml", "ocaml_interface", "python", "rust",
        "javascript", "html", "css",
      })
      vim.api.nvim_create_autocmd("FileType", {
        group = vim.api.nvim_create_augroup("LanguageSyntaxHighlighting", { clear = true }),
        pattern = { "ocaml", "ocamlinterface", "python", "rust", "javascript", "javascriptreact", "html", "css" },
        callback = function(event)
          -- Keep regular syntax highlighting if a parser is not installed yet.
          local language
          if vim.bo[event.buf].filetype == "ocaml"
            and vim.api.nvim_buf_get_name(event.buf):match("%.mli$") then
            language = "ocaml_interface"
          end
          pcall(vim.treesitter.start, event.buf, language)
        end,
      })
    end,
  },
}
