FROM oven/bun:1.4.2-alpine AS builder
WORKDIR /app
COPY package.json bun.lock ./
RUN bun install --frozen-lockfile
COPY . .
RUN bun run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY --from=builder /app/.astro/nginx-csp.conf /etc/nginx/security-csp.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
