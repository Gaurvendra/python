
const $ = (s) => document.querySelector(s);
const content = $("#content");
const sidebar = $("#sidebar");
const search = $("#search");
const themeSel = $("#theme");
const menuBtn = $("#menu");
const backdrop = $("#backdrop");
const progress = $("#progress");
const THEMES = ["light", "dark", "sepia", "midnight"];
const DONE_KEY = "pm-done";

let index = null;
const bySlug = new Map();
const cache = new Map();

// ---------- Theme ----------
function setTheme(t) {
  if (!THEMES.includes(t)) t = "light";
  document.documentElement.dataset.theme = t;
  themeSel.value = t;
  try { localStorage.setItem("pm-theme", t); } catch {}
}
themeSel.addEventListener("change", (e) => setTheme(e.target.value));
setTheme(document.documentElement.dataset.theme);

// ---------- Viewer-only progress (localStorage; no content is stored) ----------
const done = new Set(JSON.parse((() => { try { return localStorage.getItem(DONE_KEY); } catch { return null; } })() || "[]"));
function markDone(slug) {
  done.add(slug);
  try { localStorage.setItem(DONE_KEY, JSON.stringify([...done])); } catch {}
}

// ---------- Sidebar ----------
function buildSidebar(activeSlug) {
  const groups = index.modules.map((m) => {
    const items = m.pages.map((s) => {
      const p = bySlug.get(s);
      const cls = [s === activeSlug ? "active" : "", done.has(s) ? "done" : ""].join(" ").trim();
      return `<li><a class="${cls}" href="#/${s}" data-slug="${s}">${escape(p.title)}</a></li>`;
    }).join("");
    const open = m.pages.includes(activeSlug) ? " open" : "";
    return `<details class="module"${open}><summary><span>${escape(prettyModule(m.title))}</span><span class="count">${m.pages.length}</span></summary><ul>${items}</ul></details>`;
  }).join("");
  sidebar.innerHTML = groups;
}

const prettyModule = (t) => t.replace(/^\d+\s*/, "");
const escape = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

// ---------- Search ----------
search.addEventListener("input", () => {
  const q = search.value.trim().toLowerCase();
  if (!q) { buildSidebar(currentSlug()); return; }
  const hits = index.pages.filter((p) => p.title.toLowerCase().includes(q) || p.module.toLowerCase().includes(q)).slice(0, 60);
  sidebar.innerHTML = `<div class="search-results">${hits.map((p) =>
    `<a href="#/${p.slug}"><strong>${escape(p.title)}</strong><small>${escape(prettyModule(p.module))} · ${p.cells} cells</small></a>`).join("") || `<p class="loading">No lessons match “${escape(q)}”.</p>`}</div>`;
});

// ---------- Routing ----------
const currentSlug = () => decodeURIComponent(location.hash.replace(/^#\/?/, ""));

function closeMenu() { sidebar.classList.remove("open"); backdrop.classList.remove("show"); menuBtn.setAttribute("aria-expanded", "false"); }
menuBtn.addEventListener("click", () => {
  const open = !sidebar.classList.contains("open");
  sidebar.classList.toggle("open", open); backdrop.classList.toggle("show", open);
  menuBtn.setAttribute("aria-expanded", String(open));
});
backdrop.addEventListener("click", closeMenu);
sidebar.addEventListener("click", (e) => { if (e.target.closest("a")) closeMenu(); });

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const el = document.createElement("script");
    el.src = src; el.onload = () => resolve(); el.onerror = () => reject(new Error("failed to load " + src));
    document.head.appendChild(el);
  });
}

async function loadPage(slug) {
  if (cache.has(slug)) return cache.get(slug);
  const store = (window.__PM = window.__PM || { pages: {} });
  if (!(slug in store.pages)) await loadScript(`content/${slug}.js`);
  const html = store.pages[slug];
  if (html === undefined) throw new Error("empty lesson");
  cache.set(slug, html);
  return html;
}

function homeView() {
  const total = index.pages.length;
  const cards = index.modules.map((m) => {
    const first = bySlug.get(m.pages[0]);
    return `<a class="card" href="#/${first ? first.slug : ""}"><span class="n">${m.pages.length} lessons</span><h3>${escape(prettyModule(m.title))}</h3><p>${escape(first ? first.title : "")}</p></a>`;
  }).join("");
  return `<section class="home"><div class="hero"><h1>Learn Python, step by step</h1>
    <p>A structured course from your first <code>print()</code> to advanced internals, packaging, concurrency and Pydantic — every lesson is a real, executed Jupyter notebook.</p>
    <div class="stats"><span>📚 ${total} notebooks</span><span>🧭 ${index.modules.length} modules</span><span>✅ ${done.size} completed</span></div>
    <p><a href="#/${index.modules[0].pages[0]}">▶ Start with lesson 1</a></p></div>
    <div class="cards">${cards}</div></section>`;
}

function neighbours(slug) {
  const i = index.pages.findIndex((p) => p.slug === slug);
  return { prev: index.pages[i - 1], next: index.pages[i + 1] };
}

async function route() {
  const slug = currentSlug();
  if (!slug) {
    buildSidebar("");
    content.innerHTML = homeView();
    document.title = "Python Mastery";
    progress.style.width = "0%";
    window.scrollTo(0, 0);
    return;
  }
  const page = bySlug.get(slug);
  if (!page) {
    content.innerHTML = `<p class="notfound">Lesson not found. <a href="#/">Back to the course home</a>.</p>`;
    return;
  }
  buildSidebar(slug);
  content.innerHTML = `<p class="loading">Loading lesson…</p>`;
  try {
    const body = await loadPage(slug);
    const { prev, next } = neighbours(slug);
    const i = index.pages.indexOf(page) + 1;
    const mod = index.modules.find((m) => m.pages.includes(slug));
    content.innerHTML = `
      <div class="crumbs"><a href="#/">Home</a> › ${escape(prettyModule(page.module))} › lesson ${i} of ${index.pages.length}</div>
      <div class="lesson-meta"><span class="pill">📘 ${escape(prettyModule(mod ? mod.title : ""))}</span><span class="pill">🧩 ${page.cells} cells</span><span class="pill">📄 ${escape(page.file)}</span></div>
      <article class="notebook">${body}</article>
      <nav class="pager">
        ${prev ? `<a href="#/${prev.slug}"><small>← Previous</small>${escape(prev.title)}</a>` : "<span></span>"}
        ${next ? `<a class="next" href="#/${next.slug}"><small>Next →</small>${escape(next.title)}</a>` : ""}
      </nav>`;
    document.title = `${page.title} · Python Mastery`;
    markDone(slug);
    buildSidebar(slug);
    window.scrollTo(0, 0);
    content.focus({ preventScroll: true });
  } catch (err) {
    content.innerHTML = `<p class="notfound">Could not load this lesson (${escape(err.message)}).</p>`;
  }
}

// Reading progress across the page.
window.addEventListener("scroll", () => {
  const h = document.documentElement;
  const max = h.scrollHeight - h.clientHeight;
  progress.style.width = max > 0 ? `${(h.scrollTop / max) * 100}%` : "0%";
}, { passive: true });

window.addEventListener("hashchange", () => { search.value = ""; route(); });

// Keyboard: ← / → move between lessons when not typing.
window.addEventListener("keydown", (e) => {
  if (e.target.matches("input, select, textarea")) return;
  const slug = currentSlug();
  if (!slug) return;
  const { prev, next } = neighbours(slug);
  if (e.key === "ArrowRight" && next) location.hash = `#/${next.slug}`;
  if (e.key === "ArrowLeft" && prev) location.hash = `#/${prev.slug}`;
});

// ---------- Boot ----------
(async () => {
  if (!(window.__PM && window.__PM.index)) await loadScript("content/index.js");
  index = window.__PM.index;
  index.pages.forEach((p) => bySlug.set(p.slug, p));
  await route();
})();
