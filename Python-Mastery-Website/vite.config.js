import { defineConfig } from "vite";

// Emit a classic script (not an ES module) so the built site also works when
// index.html is opened directly from disk (file://), not only over HTTP.
const classicScript = () => ({
  name: "classic-script",
  enforce: "post",
  transformIndexHtml(html) {
    return html
      .replace(/<script type="module" crossorigin/g, "<script defer")
      .replace(/<link rel="stylesheet" crossorigin/g, '<link rel="stylesheet"');
  },
});

export default defineConfig({
  base: "./",
  plugins: [classicScript()],
  build: {
    outDir: "dist",
    emptyOutDir: true,
    modulePreload: false,
    rollupOptions: { output: { format: "iife", inlineDynamicImports: true } },
  },
});
