FROM oven/bun:1.4.2-alpine AS builder
WORKDIR /app
COPY package.json bun.lock ./
RUN bun install --frozen-lockfile
COPY . .
RUN bun run build

FROM oven/bun:1.4.2-alpine AS likes
USER root
WORKDIR /app
RUN mkdir /data && chown bun:bun /data
COPY --from=builder /app/.astro/likeable-posts.json .astro/likeable-posts.json
COPY scripts/likes.mjs scripts/likes.mjs
ENV LIKES_HOST=0.0.0.0 LIKES_DB=/data/likes.sqlite
USER bun
CMD ["bun", "scripts/likes.mjs"]

FROM nginx:alpine AS blog
COPY --from=builder /app/dist /usr/share/nginx/html
COPY --from=builder /app/.astro/nginx-csp.conf /etc/nginx/security-csp.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
