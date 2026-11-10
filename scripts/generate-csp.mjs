import { createHash } from 'node:crypto';

const scriptHashes = new Set();
const styleHashes = new Set();

function collectHashes(hashes) {
  let content = '';

  return {
    element(element) {
      element.onEndTag(() => {
        if (content) {
          const hash = createHash('sha256').update(content.replace(/\r\n?/g, '\n')).digest('base64');
          hashes.add(`'sha256-${hash}'`);
        }
        content = '';
      });
    },
    text(chunk) {
      content += chunk.text;
    },
  };
}

const rewriter = new HTMLRewriter()
  .on('script:not([src]):not([type="application/ld+json"])', collectHashes(scriptHashes))
  .on('style', collectHashes(styleHashes));

for await (const path of new Bun.Glob('**/*.html').scan('dist')) {
  rewriter.transform(await Bun.file(`dist/${path}`).text());
}

const policy = [
  "default-src 'none'",
  ["script-src 'self' https://analytics.vazio.club", ...[...scriptHashes].sort()].join(' '),
  ["style-src 'self' https://fonts.googleapis.com", ...[...styleHashes].sort()].join(' '),
  "font-src 'self' https://fonts.gstatic.com",
  "img-src 'self' data: https://lastfm-img.freetls.fastly.net https://tile.openstreetmap.org https://cdn.awsli.com.br https://m.media-amazon.com https://www.ultimateperformance.com.br",
  "connect-src 'self' https://analytics.vazio.club",
  "manifest-src 'self'",
  "base-uri 'none'",
  "form-action 'none'",
  "frame-ancestors 'none'",
].join('; ');

await Bun.write('.astro/nginx-csp.conf', `add_header Content-Security-Policy-Report-Only "${policy}" always;\n`);
