return {
  {
    "saghen/blink.cmp",
    tag = "v1.10.2",
    lazy = false,
    opts = {
      keymap = {
        preset = "none",
        ["<C-Space>"] = { "show", "show_documentation", "hide_documentation" },
        ["<C-n>"] = { "select_next", "fallback" },
        ["<C-p>"] = { "select_prev", "fallback" },
        ["<Down>"] = { "select_next", "fallback" },
        ["<Up>"] = { "select_prev", "fallback" },
        ["<C-y>"] = { "select_and_accept", "fallback" },
        ["<C-e>"] = { "hide", "fallback" },
      },
      sources = {
        default = { "lsp" },
        providers = {
          lsp = {
            transform_items = function(_, items)
              return vim.tbl_filter(function(item)
                return item.insertTextFormat ~= 2 and item.kind ~= 15
              end, items)
            end,
          },
        },
      },
      completion = {
        list = { selection = { preselect = false, auto_insert = false } },
        menu = { draw = { columns = { { "label", "label_description", gap = 1 }, { "kind" } } } },
        accept = { auto_brackets = { enabled = false } },
        documentation = { auto_show = true },
      },
      fuzzy = { implementation = "lua" },
      cmdline = { enabled = false },
    },
  },
}
