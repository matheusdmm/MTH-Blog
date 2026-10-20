import { getCollection, type CollectionEntry } from 'astro:content';

export async function getPhotos() {
  return (await getCollection('img')).sort(
    (a, b) => b.data.date.valueOf() - a.data.date.valueOf() || a.id.localeCompare(b.id),
  );
}

export function getRelatedPhotos(photo: CollectionEntry<'img'>, photos: CollectionEntry<'img'>[]) {
  const tags = new Set(photo.data.tags);
  return photos
    .filter((candidate) => candidate.id !== photo.id)
    .map((candidate) => ({
      photo: candidate,
      shared: [...new Set(candidate.data.tags)].filter((tag) => tags.has(tag)).length,
    }))
    .filter((candidate) => candidate.shared > 0)
    .sort((a, b) => b.shared - a.shared
      || b.photo.data.date.valueOf() - a.photo.data.date.valueOf()
      || a.photo.id.localeCompare(b.photo.id))
    .slice(0, 3)
    .map((candidate) => candidate.photo);
}
