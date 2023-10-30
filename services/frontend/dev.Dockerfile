# build stage
FROM alpine
RUN curl -fsSL https://bun.sh/install | bash
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
