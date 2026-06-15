---
title: 'Construindo o blog'
description: 'Escolhas de design, Um pouco do Astro e porque foi massa fazer isso.'
pubDate: 'May 02 2026'
tags: ['dev']
heroImage: 'https://images.unsplash.com/photo-1548755343-4e4e6f6515c2?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
---

Tudo começou com um diagnostico de bursite um dia antes do feriado do dia do trabalhador. Eu tava nostalgico em relação as coisas que eu gostava quando tava aprendendo sobre a internet.

Eu tinha alguns blogs beeeem antes disso ser `mainstream ou cool`. Hosteava eles na antiga Uol Zip.Net, Wordpress ou no Blogger/Blogspot (antes do google comprar). De certo modo, foi minha porta de entrada pra programação.

Com isso em mente, eu comecei a juntar algumas possibilidades. Queria um site que fosse rapido, facil de manter e que visualmente se parecece com o que eu queria. Sem temas, sem CMS de arrastar e soltar, sem porra nenhuma. Isso nos trás até o presente momento.

## A stack

O blog roda em cima do [Astro](https://astro.build), um gerador de sites estáticos que builda um total de zero JavaScript (olha a ironia, visto que foi por causa dele que eu tenho um trabalho hoje em dia) por padrão. As únicas dependências são:

- `@astrojs/mdx` — Escreve os posts em Markdown com JSX se eu quiser
- `@astrojs/rss` — RSS Automático feed em `/rss.xml`
- `@astrojs/sitemap` — Mapa do site
- `sharp` — Otimização de imagens durante a build
- `tailwindcss` — Base de reset e utilitários CSS

Sem nenhum framework de UI, sem nenhum runtime de JS no cliente, a não ser que eu precise adicionar em uma página específica.

## Escolhas de design

A estética é minimalista e deliberada — cantos levemente arredondados, sombras sutis, sem explosão visual. Queria que parecesse uma leitura confortável, não um painel de controle.

O sistema de temas usa dois esquemas de cores distintos: **Nord Light** para o tema claro e **Ayu Dark** para o escuro. Escolhas bem diferentes em temperatura e personalidade, mas que funcionam bem nos dois extremos.

```css
:root {
  /* Nord Light */
  --bg:       #ECEFF4;
  --fg:       #2E3440;
  --fg-muted: #4C566A;
  --accent:   #5E81AC;
  --border:   rgba(46, 52, 64, 0.14);
}

[data-theme="dark"] {
  /* Ayu Dark */
  --bg:       #0A0E14;
  --fg:       #B3B1AD;
  --fg-muted: #626A73;
  --accent:   #FF8F40;
  --border:   rgba(179, 177, 173, 0.08);
}
```

Para fontes, a combinação que funcionou:

- **Inter** — UI, títulos, navegação
- **Lora** — corpo dos posts (serifada, muito mais legível pra textos longos)
- **JetBrains Mono** — snippets de código

Quando o tema é alterado, o atributo `data-theme` é escrito no `<html>` e a escolha é salva no `localStorage`. Todo componente novo que eu adicionar herda os tokens sem precisar escrever variantes dark/light separadas.

## Como o Astro funciona

O Astro utiliza um roteador baseado em arquivos. Um arquivo em `src/pages/blog/index.astro` torna-se `/blog`. As páginas são componentes .astro.

Os posts do blog ficam em `src/content/blog/` como arquivos Markdown ou MDX. As **Content Collections** do Astro impõem um esquema ao frontmatter para que o TypeScript conheça a estrutura de cada post em tempo de build:

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
    hidden: z.boolean().optional(),
  }),
});
```

Armazenando os posts e então sorteando eles durante a build, eu posso inclusive esconder posts que estão em desenvolvimento ou revisão:

```ts
const posts = (await getCollection('blog'))
  .filter((post) => !post.data.hidden)
  .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
```

Sem banco de dados, sem API, só arquivos.

## Configuração

`astro.config.mjs` é onde todas as integrações são registradas:

```js
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://yourdomain.com',
  integrations: [mdx(), sitemap()],
});
```

Configurando o `site` é necessario pro mapa do site e pro RSS, ele vai gerar as URLs corretamente.

As globais vivem em `src/consts.ts`e são importadas sempre que necessario, só tem um lugar pra se preocupar em atualizar tudo.

## Porque Astro

**O output é HTML estático.** Sem servidor para manter, sem _cold starts_. Faça o deploy na Vercel, Netlify ou qualquer CDN com `npm run build`.

**Zero JS por padrão.** O client baixa apenas o que for estritamente necessário. Componentes interativos podem ser habilitados com as diretivas `client:load` ou `client:idle`.

**Markdown é simplificar.** Escrever um post é criar um arquivo `.md`. A validação captura os erros no _frontmatter_ antes mesmo do build ser finalizado.

**Complexidade incremental.** O blog não possui configuração de _bundler_, gerenciamento de estado ou rotas de API. Se ele crescer e precisar disso, o Astro suporta sem exigir um _rewrite_, do contrário, continua sendo um HTML simples.

**O tradeoff:** não tem _live preview_ em GUI e nem painel admin. Os posts são escritos em um editor de texto e commitados no git. Isso é um feature, não um bug. Uma forma de pensar.

Isso é a maneira mais minimalista que eu encontrei na web moderna para me expressar. De longe lembra um pouco a epoca do FTP. Massa demais.

Valeu demais, continua arrasando 🤘- Matheus.
