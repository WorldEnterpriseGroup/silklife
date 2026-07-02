# Repository Guidelines

## Project Structure & Module Organization
This is a static HTML magazine site. Core pages live at the repo root (`index.html`, `category-*.html`, `post-*.html`). Styles are in `style/`, scripts in `js/`, and images in `images/` (article and homepage assets). Supporting content files like `CHARACTERS.md`, `article_catalog.csv`, and processing reports live at the root. Shell/Python utilities for content and image maintenance are also at the root (for example `generate_articles.py`, `optimize_images.sh`).

## Build, Test, and Development Commands
- `python -m http.server 8000` - serve the site locally for quick previews.
- `npx serve` - alternative local static server (requires Node).
- `./check_homepage_images.sh` - list homepage images still at 1024x1024 (uses ImageMagick).
- `./optimize_images.sh` - resize a known set of homepage assets with backups.

## Coding Style & Naming Conventions
Keep existing formatting in each file. HTML uses tab indentation and compact attribute formatting; CSS uses Allman-style braces and mixes tabs/spaces—preserve local style when editing. File naming patterns are important:
- Articles: `post-[category]-[topic].html` (example: `post-yoga-morning-flow.html`).
- Categories: `category-[name].html`.
- Images: `images/articles/[category]-[topic].webp` and `images/homepage/hp-[topic]-[nn]-[size].webp`.

## Image Generation
Use the Nanobanana MCP for all image generation: `mcp__nanobanana__generate_image`.

## Testing Guidelines
There is no automated test suite. Validate changes by running a local server and checking:
- page rendering in desktop and mobile widths
- links and navigation updates
- image dimensions and load performance

## Commit & Pull Request Guidelines
Recent commit messages use short, imperative, sentence-case summaries (example: “Redesign subscribe page and update navigation across pages”). Follow that style. For PRs, include a clear summary, list the pages touched, and attach before/after screenshots for visual changes. If you add or update content, note any new characters or images and their filenames.

## Content & Brand Rules
This site is set in the **Mid-Ohio Valley** (always use that exact name). Before writing or updating articles, consult `CHARACTERS.md` and use established character names and locations. Keep stories first-person, specific, and grounded in Victorian cottage details; avoid generic wellness copy or professional instruction.
