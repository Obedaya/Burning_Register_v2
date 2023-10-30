# build stage
FROM oven/bun:latest
WORKDIR /app
COPY package.json ./
COPY bun.lockb ./
COPY babel.config.js ./
COPY jsconfig.json ./
COPY vue.config.js ./
COPY .eslintrc.js ./


RUN bun install
COPY src ./src
CMD ["bun", "serve"]
