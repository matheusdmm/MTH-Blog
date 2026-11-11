import type { APIRoute } from 'astro';
import { getEntry } from 'astro:content';
import { createLikesHandler } from './likes.mjs';

export const prerender = false;

const handleLikes = createLikesHandler(async (id: string) => {
  const post = await getEntry('blog', id);
  return post !== undefined && !post.data.hidden;
});

export const ALL: APIRoute = ({ request }) => handleLikes(request);
