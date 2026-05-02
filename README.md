# MATHEUSDMM

Personal blog and portfolio built with [Astro](https://astro.build).

## Stack

- **Astro 6** — static site generator, zero JS by default
- **@astrojs/mdx** — Markdown + JSX for blog posts
- **@astrojs/rss** — RSS feed at `/rss.xml`
- **@astrojs/sitemap** — auto-generated sitemap
- **sharp** — build-time image optimization

## Pages

| Route | Description |
| :---- | :---------- |
| `/` | Home / landing |
| `/blog` | Post listing |
| `/blog/[slug]` | Individual post |
| `/projects` | Project cards |
| `/about` | Resume / profile |

## Project structure

```
src/
├── assets/
│   └── fonts/          # Local font files
├── components/         # Astro components (Header, Footer, BaseHead…)
├── content/
│   └── blog/           # Markdown/MDX posts — add files here
├── layouts/            # BlogPost layout
├── pages/              # File-based routes
└── styles/
    └── global.css      # Design tokens, base styles
astro.config.mjs
```

## Commands

```sh
npm install        # Install dependencies
npm run dev        # Dev server at localhost:4321
npm run build      # Production build to ./dist/
npm run preview    # Preview the production build locally
```

## Design

Brutalist aesthetic: high-contrast black/white, hard `4px 4px 0` offset shadows with no blur, zero border-radius, monospace UI labels. Light/dark theme driven by two CSS custom properties (`--bg` / `--fg`) toggled via `data-theme` on `<html>`.

## Fonts

### Redaction — body text

Designed by **Forest Young** (Wolff Olins) and **Jeremy Mickel** (MCKL), commissioned for the book *Until* by Reginald Dwayne Betts.

Licensed under the [SIL Open Font License 1.1](https://openfontlicense.org). You are free to use, study, modify, and redistribute this font, including in commercial projects, provided derivative fonts are released under the same license and the font is not sold on its own.

Source: [https://www.redaction.us](https://www.redaction.us)

### JetBrains Mono — code blocks

Designed by **JetBrains**, served via Google Fonts.

Licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). You are free to use this font for any purpose, including commercial use, modification, and redistribution.

Source: [https://www.jetbrains.com/lp/mono](https://www.jetbrains.com/lp/mono)
