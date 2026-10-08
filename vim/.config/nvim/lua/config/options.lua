local opt = vim.opt
opt.termguicolors = true
opt.background = "dark"

opt.number = true
opt.relativenumber = true
opt.expandtab = true
opt.tabstop = 2
opt.shiftwidth = 2
opt.softtabstop = 2
opt.autoindent = true

opt.ignorecase = true
opt.smartcase = true
opt.hlsearch = true
opt.incsearch = true
opt.undofile = true

opt.scrolloff = 8
opt.wrap = false
opt.cursorline = true
opt.signcolumn = "yes"

-- Reload external edits only when the buffer has no unsaved changes.
opt.autoread = true
vim.api.nvim_create_autocmd({ "FocusGained", "BufEnter" }, {
  group = vim.api.nvim_create_augroup("ReloadExternalChanges", { clear = true }),
  desc = "Check for external file changes when returning to Neovim",
  callback = function()
    if vim.fn.getcmdwintype() == "" then
      vim.cmd("checktime")
    end
  end,
})

-- Keep ordinary registers usable when no system clipboard is available.
if vim.fn.has("clipboard") == 1 then
  opt.clipboard = "unnamedplus"
end
