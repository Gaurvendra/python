// Converts every .ipynb in the course folder into a static HTML fragment.
// READ-ONLY with respect to the course: notebooks are only read, never written.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { Marked } from "marked";
import hljs from "highlight.js/lib/common";

const here = path.dirname(fileURLToPath(import.meta.url));
const COURSE = path.resolve(process.env.COURSE_DIR || path.join(here, "../Python-Mastery-Course"));
const OUT = path.join(here, "../public/content");

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const ANSI = /\x1b\[[0-9;?]*[A-Za-z]|\x1b\]8;[^\x1b\x07]*(?:\x1b\\|\x07)/g;

const marked = new Marked({ gfm: true, breaks: false });
// Syntax-highlight fenced code blocks inside markdown cells.
marked.use({
  renderer: {
    code(token) {
      const lang = (token.lang || "").split(/\s+/)[0];
      const known = lang && hljs.getLanguage(lang);
      const html = known ? hljs.highlight(token.text, { language: lang }).value : esc(token.text);
      return `<pre class="code-block"><code class="hljs language-${esc(lang || "plaintext")}">${html}</code></pre>\n`;
    },
  },
});

const text = (v) => (Array.isArray(v) ? v.join("") : v || "");

function highlightCode(src) {
  return hljs.highlight(src, { language: "python" }).value;
}

function renderOutput(out) {
  if (out.output_type === "stream") {
    const cls = out.name === "stderr" ? "out-stderr" : "out-stdout";
    return `<pre class="output ${cls}">${esc(text(out.text).replace(ANSI, ""))}</pre>`;
  }
  if (out.output_type === "error") {
    const tb = (out.traceback || []).join("\n").replace(ANSI, "");
    return `<pre class="output out-error">${esc(tb || `${out.ename}: ${out.evalue}`)}</pre>`;
  }
  const data = out.data || {};
  if (data["image/png"]) return `<figure class="output out-image"><img alt="notebook output" src="data:image/png;base64,${data["image/png"].replace(/\s/g, "")}"></figure>`;
  if (data["image/jpeg"]) return `<figure class="output out-image"><img alt="notebook output" src="data:image/jpeg;base64,${data["image/jpeg"].replace(/\s/g, "")}"></figure>`;
  if (data["image/svg+xml"]) return `<figure class="output out-image">${text(data["image/svg+xml"])}</figure>`;
  if (data["text/html"]) return `<div class="output out-html">${text(data["text/html"])}</div>`;
  if (data["text/plain"]) return `<pre class="output out-result">${esc(text(data["text/plain"]).replace(ANSI, ""))}</pre>`;
  return "";
}

function renderNotebook(nb) {
  const parts = [];
  let n = 0;
  for (const cell of nb.cells) {
    const src = text(cell.source);
    if (cell.cell_type === "markdown") {
      parts.push(`<section class="cell md">${marked.parse(src)}</section>`);
    } else if (cell.cell_type === "code") {
      n += 1;
      const tags = cell.metadata?.tags || [];
      const note = tags.includes("raises-exception") ? `<span class="badge badge-error">expected error</span>`
        : tags.includes("skip-execution") ? `<span class="badge badge-skip">run it yourself</span>` : "";
      const outs = (cell.outputs || []).map(renderOutput).join("");
      parts.push(
        `<section class="cell code">` +
        `<div class="cell-head"><span class="prompt">In [${cell.execution_count ?? " "}]:</span>${note}</div>` +
        `<pre class="code-block"><code class="hljs language-python">${highlightCode(src)}</code></pre>` +
        (outs ? `<div class="outputs"><span class="prompt">Out:</span>${outs}</div>` : "") +
        `</section>`
      );
    }
  }
  return parts.join("\n");
}

function titleOf(nb, fallback) {
  for (const c of nb.cells) {
    if (c.cell_type === "markdown") {
      const m = text(c.source).match(/^#\s+(.+)$/m);
      if (m) return m[1].replace(/[*_`]/g, "").trim();
    }
  }
  return fallback;
}

const humanize = (s) => s.replace(/^\d+[-_]?/, "").replace(/[-_]+/g, " ").replace(/\.ipynb$/, "").trim();

// Walk the course tree. Module folders become sections; notebooks become pages.
function walk(dir, rel = "") {
  const entries = fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name, undefined, { numeric: true }));
  const files = [];
  const dirs = [];
  for (const e of entries) {
    if (e.name.startsWith(".")) continue;
    if (e.isDirectory()) dirs.push(e);
    else if (e.isFile() && e.name.endsWith(".ipynb") && !e.name.includes("checkpoint")) files.push(e);
  }
  return { files, dirs };
}

fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });

const pages = [];
const modules = [];

function collect(dir, relDir, moduleTitle) {
  const { files, dirs } = walk(dir);
  for (const f of files) {
    const abs = path.join(dir, f.name);
    const relPath = path.join(relDir, f.name);
    const slug = relPath.replace(/\.ipynb$/, "").replace(/[^a-zA-Z0-9]+/g, "-").toLowerCase();
    const nb = JSON.parse(fs.readFileSync(abs, "utf8"));
    const title = titleOf(nb, humanize(f.name));
    const cells = nb.cells.length;
    fs.writeFileSync(path.join(OUT, `${slug}.html`), renderNotebook(nb));
    pages.push({ slug, title, module: moduleTitle, file: relPath, cells, order: pages.length });
  }
  for (const d of dirs) {
    if (d.name === "exercises") continue;
    collect(path.join(dir, d.name), path.join(relDir, d.name), moduleTitle || humanize(d.name));
  }
}

// Top-level modules (folders NN-Name) in order.
const top = fs.readdirSync(COURSE, { withFileTypes: true })
  .filter((e) => e.isDirectory() && /^\d{2}-/.test(e.name))
  .sort((a, b) => a.name.localeCompare(b.name));

for (const d of top) {
  const title = humanize(d.name);
  const before = pages.length;
  collect(path.join(COURSE, d.name), d.name, title);
  modules.push({ id: d.name, title, pages: pages.slice(before).map((p) => p.slug) });
}

// Exercise notebooks are listed as their own pages too, so nothing is hidden.
for (const d of top) {
  const ex = path.join(COURSE, d.name, "exercises");
  if (!fs.existsSync(ex)) continue;
  const before = pages.length;
  const { files } = walk(ex);
  for (const f of files) {
    const abs = path.join(ex, f.name);
    const relPath = path.join(d.name, "exercises", f.name);
    const slug = relPath.replace(/\.ipynb$/, "").replace(/[^a-zA-Z0-9]+/g, "-").toLowerCase();
    const nb = JSON.parse(fs.readFileSync(abs, "utf8"));
    fs.writeFileSync(path.join(OUT, `${slug}.html`), renderNotebook(nb));
    pages.push({ slug, title: titleOf(nb, humanize(f.name)), module: humanize(d.name), file: relPath, cells: nb.cells.length, order: pages.length });
  }
  const mod = modules.find((m) => m.id === d.name);
  if (mod) mod.pages.push(...pages.slice(before).map((p) => p.slug));
}

const indexData = { generated: new Date().toISOString(), modules, pages };
fs.writeFileSync(path.join(OUT, "index.json"), JSON.stringify(indexData, null, 1));

// Script versions of every page: these also work when the site is opened straight from disk (file://),
// where browsers block fetch(). Each file registers its HTML on window.__PM.
fs.writeFileSync(path.join(OUT, "index.js"), `window.__PM=window.__PM||{pages:{}};window.__PM.index=${JSON.stringify(indexData)};`);
for (const p of pages) {
  const html = fs.readFileSync(path.join(OUT, `${p.slug}.html`), "utf8");
  fs.writeFileSync(path.join(OUT, `${p.slug}.js`), `window.__PM=window.__PM||{pages:{}};window.__PM.pages[${JSON.stringify(p.slug)}]=${JSON.stringify(html)};`);
}
console.log(`Rendered ${pages.length} notebooks in ${modules.length} modules → ${path.relative(process.cwd(), OUT)}`);
