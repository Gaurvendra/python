# Python Mastery — Website

A static, responsive learning site that displays every notebook of the
Python Mastery Course. Notebooks are read-only inputs; the site never writes
to the course folder.

## Use

```bash
npm install
npm run dev        # local development (http://localhost:5173)
npm run build      # produces dist/ — a fully static site
npm run preview    # serve dist/ locally
```

`npm run build` first renders every `.ipynb` in `../Python-Mastery-Course`
into `public/content/*.html` (markdown, code, outputs, images, errors) and an
`index.json` table of contents. To use another location:
`COURSE_DIR=/path/to/notebooks npm run build`.

## Open without a server

The built site also works by double-clicking `dist/index.html` (no web server needed).

## Docker

```bash
docker compose up --build   # http://localhost:8082 (the host port set in docker-compose.yml)
```

## Deploy

`dist/` is plain HTML/CSS/JS with relative paths, so it works on GitHub Pages,
Netlify, Cloudflare Pages or any web server — no backend needed.

## Features

- Four themes: Light, Dark, Sepia, Midnight (remembered per browser)
- Sidebar course tree with module folders, search, and completed-lesson ticks
- Previous/next navigation, ← / → keyboard shortcuts, reading progress bar
- Responsive layout: the sidebar becomes a slide-out menu on phones
- Notebook outputs (text, errors, plots/images) shown exactly as saved
