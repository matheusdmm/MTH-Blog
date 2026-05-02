---
title: 'Building this blog'
description: 'Design choices, Astro internals, and why it was worth it'
pubDate: 'May 02 2025'
heroImage: 'https://images.unsplash.com/photo-1548755343-4e4e6f6515c2?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
---

It all started with a bursitis, a day before labors day holliday. I was remembering things I used to like when I was still learning things on the internet. 

I had a couple of blogs way before it was a big thing. Hosted blogs on the old Uol Zip.Net, Wordpress and Blogger/Blogspot (before google bought them).

With this in mind, I started to scratch a couple Ideas. I wanted a site that was fast, easy to maintain, and looked exactly how I wanted — no themes, no CMS drag-and-drop, no bullshit. This is what I ended up with and how it works.

## The stack

The blog runs on [Astro](https://astro.build), a static site generator that ships zero JavaScript (the irony, seeing that javascript was my entrypoint to tech) by default. The only dependencies are:

- `@astrojs/mdx` — write posts in Markdown with JSX components if needed
- `@astrojs/rss` — automatic RSS feed at `/rss.xml`
- `@astrojs/sitemap` — sitemap for SEO
- `sharp` — local image optimization at build time

No framework, no runtime JS on the client unless you explicitly add it.

## Design choices

The aesthetic is deliberately brutalist: hard edges, no border-radius anywhere, a `4px 4px 0` offset box shadow that moves with the theme instead of blurring out, and Courier New for all metadata (dates, tags, labels). The main body font is Atkinson — designed for readability.

The palette is two CSS custom properties, `--bg` and `--fg`, that flip on `[data-theme="dark"]`. Everything else derives from those two values. This means adding dark mode to any new component is essentially free.

```css
:root {
    --bg: #ffffff;
    --fg: #000000;
    --shadow: 4px 4px 0 var(--fg);
}

[data-theme="dark"] {
    --bg: #0d0d0d;
    --fg: #f0f0f0;
}
```

The theme toggle writes `data-theme` to `<html>` and persists the choice in `localStorage`.

## How Astro works

Astro uses a file-based router. A file at `src/pages/blog/index.astro` becomes `/blog`. Pages are `.astro` components — a fenced frontmatter block for imports and logic, then HTML-like template below.

Blog posts live in `src/content/blog/` as Markdown or MDX files. Astro's **Content Collections** enforce a schema on the frontmatter so TypeScript knows the shape of every post at build time:

```ts
// src/content.config.ts
const blog = defineCollection({
    type: 'content',
    schema: z.object({
        title: z.string(),
        description: z.string(),
        pubDate: z.coerce.date(),
        updatedDate: z.coerce.date().optional(),
        heroImage: z.string().optional(),
    }),
});
```

Querying posts is then typed and sorted at build time:

```ts
const posts = (await getCollection('blog'))
    .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
```

No database, no API — just files.

## Configuration

`astro.config.mjs` is where integrations are registered:

```js
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
    site: 'https://yourdomain.com',
    integrations: [mdx(), sitemap()],
});
```

Setting `site` is required for the sitemap and RSS feed to generate absolute URLs correctly.

Global constants (site title, description, links) live in `src/consts.ts` and are imported wherever needed — one place to update them.

## Why Astro

**Output is static HTML.** No server to maintain, no cold starts. Deploy to Vercel, Netlify, or any CDN with `npm run build`.

**Zero JS by default.** The reader downloads only what they need. Interactive components can opt in with `client:load` or `client:idle` directives.

**Markdown is a first-class citizen.** Writing a post is creating a `.md` file. The schema validation catches typos in frontmatter before the build goes out.

**Incremental complexity.** You start simple and add only what you need. This blog has no bundler config, no state management, no API routes. If it grows to need them, Astro supports it without a rewrite.

The tradeoff: there is no live preview in a GUI and no admin panel. Posts are written in a text editor and committed to git. That is a feature, not a bug.

This is the most minimalistic way that I can find in the modern web to express myself. 

Thank you, take care and keep rocking 🤘- Matheus.
