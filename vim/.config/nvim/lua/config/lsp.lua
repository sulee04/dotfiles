vim.diagnostic.config({
  severity_sort = true,
  virtual_text = false,
  underline = true,
  update_in_insert = false,
  float = { border = "rounded", source = "if_many" },
  signs = {
    text = {
      [vim.diagnostic.severity.ERROR] = "E",
      [vim.diagnostic.severity.WARN] = "W",
      [vim.diagnostic.severity.INFO] = "I",
      [vim.diagnostic.severity.HINT] = "H",
    },
  },
})

vim.api.nvim_create_autocmd("LspAttach", {
  group = vim.api.nvim_create_augroup("LanguageServerShortcuts", { clear = true }),
  callback = function(event)
    local function map(lhs, rhs, desc)
      vim.keymap.set("n", lhs, rhs, { buffer = event.buf, desc = desc })
    end
    map("gd", function() require("telescope.builtin").lsp_definitions() end, "Go to definition")
    map("K", vim.lsp.buf.hover, "Hover documentation")
    map("<leader>cr", vim.lsp.buf.rename, "Rename symbol")
    map("<leader>ca", vim.lsp.buf.code_action, "Code action")
    map("<leader>cR", function() require("telescope.builtin").lsp_references() end, "Find references")
    map("<leader>dd", vim.diagnostic.open_float, "Show line diagnostics")
    map("<leader>dl", function() require("telescope.builtin").diagnostics({ bufnr = 0 }) end, "List buffer diagnostics")
    if vim.bo[event.buf].filetype == "lean" then
      map("<leader>lg", "<cmd>LeanGoal<CR>", "Show Lean goal")
      map("<leader>lr", "<cmd>LeanRestartFile<CR>", "Restart Lean file")
    end
  end,
})

-- Resolve ocamllsp through the project's opam switch, not a pinned switch path.
vim.lsp.config("ocamllsp", {
  filetypes = { "ocaml", "dune" },
  cmd = function(dispatchers, config)
    local cmd = vim.fn.executable("opam") == 1
      and { "opam", "exec", "--", "ocamllsp" } or { "ocamllsp" }
    return vim.lsp.rpc.start(cmd, dispatchers, { cwd = config.root_dir })
  end,
})
vim.lsp.config("basedpyright", {
  settings = { basedpyright = { analysis = { typeCheckingMode = "standard" } } },
})
vim.lsp.enable({ "ocamllsp", "basedpyright", "rust_analyzer" })
-- lean.nvim supplies and enables its own leanls configuration.
