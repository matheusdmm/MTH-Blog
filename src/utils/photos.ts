import { getCollection } from 'astro:content';

export async function getPhotos() {
  return (await getCollection('img')).sort(
    (a, b) => b.data.date.valueOf() - a.data.date.valueOf() || a.id.localeCompare(b.id),
  );
}
