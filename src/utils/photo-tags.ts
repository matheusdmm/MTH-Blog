export function photoTagUrl(tag: string) {
  return `/img?tag=${encodeURIComponent(tag)}`;
}
