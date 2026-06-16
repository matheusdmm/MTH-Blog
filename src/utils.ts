export const readTime = (body: string | undefined) =>
  body ? Math.ceil(body.split(/\s+/).filter(Boolean).length / 200) : undefined;
