import { randomUUID } from 'node:crypto';
import { mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { Database } from 'bun:sqlite';

/** @param {(post: string) => boolean | Promise<boolean>} isPublished */
export function createLikesHandler(isPublished) {
  const dbPath = process.env.LIKES_DB ?? join(dirname(fileURLToPath(import.meta.url)), '../.data/likes.sqlite');
  mkdirSync(dirname(dbPath), { recursive: true });

  const db = new Database(dbPath);
  db.run(`
    CREATE TABLE IF NOT EXISTS likes (
      post TEXT NOT NULL,
      visitor TEXT NOT NULL,
      PRIMARY KEY (post, visitor)
    ) WITHOUT ROWID;
  `);

  const state = db.query(`
    SELECT count(*) AS count, EXISTS (
      SELECT 1 FROM likes WHERE post = ?1 AND visitor = ?2
    ) AS liked
    FROM likes WHERE post = ?1
  `);
  const like = db.query('INSERT INTO likes VALUES (?, ?) ON CONFLICT DO NOTHING');
  const unlike = db.query('DELETE FROM likes WHERE post = ? AND visitor = ?');

  /** @param {Request} request */
  return async function handleLikes(request) {
    const url = new URL(request.url);
    const post = url.searchParams.get('post');
    const headers = new Headers({ 'Cache-Control': 'no-store' });
    const { method } = request;

    if (!/^\/api\/likes\/?$/.test(url.pathname) || !post || !(await isPublished(post))) {
      return new Response(null, { status: 404, headers });
    }
    if (method !== 'GET' && method !== 'PUT' && method !== 'DELETE') {
      headers.set('Allow', 'GET, PUT, DELETE');
      return new Response(null, { status: 405, headers });
    }

    const cookie = request.headers.get('cookie') ?? '';
    let visitor = /(?:^|;\s*)post_likes=([a-f0-9]{32})(?=;|$)/.exec(cookie)?.[1];
    if (!visitor) {
      if (method !== 'GET') return new Response(null, { status: 409, headers });
      visitor = randomUUID().replaceAll('-', '');
      const secure = url.protocol === 'https:' || request.headers.get('x-forwarded-proto') === 'https';
      headers.set('Set-Cookie', `post_likes=${visitor}; Path=/api/likes; Max-Age=31536000; HttpOnly; SameSite=Lax${secure ? '; Secure' : ''}`);
    }

    if (method === 'PUT') like.run(post, visitor);
    if (method === 'DELETE') unlike.run(post, visitor);

    const result = state.get(post, visitor);
    return Response.json({ count: result.count, liked: Boolean(result.liked) }, { headers });
  };
}

if (import.meta.main) {
  const posts = new Set(await Bun.file(new URL('../.astro/likeable-posts.json', import.meta.url)).json());
  const server = Bun.serve({
    hostname: process.env.LIKES_HOST ?? '127.0.0.1',
    port: 3001,
    maxRequestBodySize: 1024,
    fetch: createLikesHandler((post) => posts.has(post)),
  });
  console.log(`Curtidas: ${server.url}`);
}
