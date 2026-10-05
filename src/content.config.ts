import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const blog = defineCollection({
	loader: glob({ base: './src/content/blog', pattern: '*.{md,mdx}' }),
	schema: ({ image }) =>
		z.object({
			title: z.string(),
			description: z.string(),
			pubDate: z.coerce.date(),
			updatedDate: z.coerce.date().optional(),
		tags: z.array(z.string()).optional(),
			heroImage: z.optional(image()),
			hidden: z.boolean().optional(),
		}),
});

const img = defineCollection({
	loader: glob({ base: './src/content/img', pattern: '*.md' }),
	schema: ({ image }) =>
		z.object({
			image: image(),
			alt: z.string().min(1),
			caption: z.string().min(1),
			date: z.coerce.date(),
			title: z.string().optional(),
			tags: z.array(z.string()).default([]),
			demo: z.boolean().default(false),
			location: z.object({
				name: z.string(),
				latitude: z.number().min(-90).max(90).optional(),
				longitude: z.number().min(-180).max(180).optional(),
			}).optional(),
		}),
});

export const collections = { blog, img };
