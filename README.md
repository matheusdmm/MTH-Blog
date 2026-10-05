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
| `/img` | Photo mosaic |
| `/img/[slug]` | Individual photo and caption |
| `/projects` | Project cards |
| `/about` | Resume / profile |

## Project structure

```
src/
├── assets/
│   └── fonts/          # Local font files
├── components/         # Astro components (Header, Footer, BaseHead…)
├── content/
│   ├── blog/           # Markdown/MDX posts
│   └── img/            # Photos and their Markdown metadata
├── layouts/            # BlogPost layout
├── pages/              # File-based routes
└── styles/
    └── global.css      # Design tokens, base styles
astro.config.mjs
```

## Commands

```sh
bun install        # Install dependencies
bun run dev        # Dev server at localhost:4321
bun run build      # Production build to ./dist/
bun run preview    # Preview the production build locally
```

## Publishing a photo

Add an image and a Markdown file with the same descriptive name to `src/content/img/`. For example, `fim-de-tarde.jpg` and `fim-de-tarde.md`:

```md
---
image: ./fim-de-tarde.jpg
alt: Luz do fim de tarde atravessando a janela
caption: Uma tarde que valeu guardar.
date: 2026-10-05
title: Fim de tarde
tags: [cotidiano]
location:
  name: São Paulo, SP
  latitude: -23.5505
  longitude: -46.6333
---
```

Only `image`, `alt`, `caption`, and `date` are required. `title`, `tags`, and `location` are optional; coordinates are optional inside `location`. The file name becomes the photo URL (`/img/fim-de-tarde`). Images are optimized during the Astro build. New photos require a new build/deploy.

The current entries in `src/content/img/` are generated test photos. They use `demo: true` to show an “Exemplo” label in the mosaic; remove or replace them when publishing personal photos.

### Importador com interface gráfica

No Windows, abra `abrir-importador-img.cmd` com dois cliques. Escolha uma foto JPEG, PNG ou WebP, confira a prévia e os dados EXIF, preencha título, legenda e texto alternativo e clique em **Salvar na galeria**. A data EXIF é sugerida quando existe; você pode alterá-la.

O importador cria a imagem e o arquivo `.md` em `src/content/img/`. A cópia publicada é salva na orientação correta e sem EXIF. Coordenadas GPS só entram no `.md` se você marcar **Publicar localização exata da foto** e informar o nome do lugar. O importador não substitui posts existentes.

O launcher usa o Python disponibilizado pelo Codex neste computador. Em outra instalação, é preciso ter Python com Tkinter e Pillow. Depois de salvar, execute `bun run build` ou o fluxo normal de publicação do site.

Os posts de imagem aparecem em `/img`, separadamente do arquivo `/blog`. Com `bun run dev` aberto, atualize `http://localhost:4321/img` para vê-los. O site público só recebe o novo post depois de uma nova publicação. O importador oferece abrir a prévia local assim que salva.

## Design

Warm light theme, charcoal dark theme, copper accent, and IBM Plex Sans. The theme is selected through `data-theme` on `<html>`.

## Fonts

### Redaction — body text

Designed by **Forest Young** (Wolff Olins) and **Jeremy Mickel** (MCKL), commissioned for the book *Until* by Reginald Dwayne Betts.

Licensed under the [SIL Open Font License 1.1](https://openfontlicense.org). You are free to use, study, modify, and redistribute this font, including in commercial projects, provided derivative fonts are released under the same license and the font is not sold on its own.

Source: [https://www.redaction.us](https://www.redaction.us)

### JetBrains Mono — code blocks

Designed by **JetBrains**, served via Google Fonts.

Licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). You are free to use this font for any purpose, including commercial use, modification, and redistribution.

Source: [https://www.jetbrains.com/lp/mono](https://www.jetbrains.com/lp/mono)
