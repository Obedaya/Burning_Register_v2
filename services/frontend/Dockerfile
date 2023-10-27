# build stage
FROM oven/bun:latest as build-stage
WORKDIR /app
COPY package.json ./
COPY bun.lockb ./

RUN bun install
COPY . .
RUN bun run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]