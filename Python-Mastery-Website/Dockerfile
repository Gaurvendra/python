# syntax=docker/dockerfile:1
# Build context is the PARENT folder (so the notebooks in ../Python-Mastery-Course are visible).
# The notebooks are only read during the build; they are never modified.

# ---- 1. Build the static site ----
FROM node:22-alpine AS build
WORKDIR /app
COPY Python-Mastery-Website/package.json Python-Mastery-Website/package-lock.json ./
RUN npm ci
COPY Python-Mastery-Website/ ./
COPY Python-Mastery-Course /course
ENV COURSE_DIR=/course
RUN npm run build

# ---- 2. Serve it with nginx ----
FROM nginxinc/nginx-unprivileged:1.27-alpine AS runtime
COPY Python-Mastery-Website/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://127.0.0.1:8080/ >/dev/null || exit 1
