# build stage
FROM alpine
RUN apk add curl bash
RUN curl -fsSL https://bun.sh/install | bash
WORKDIR /app
COPY package.json ./
COPY bun.lockb ./
COPY babel.config.js ./
COPY jsconfig.json ./
COPY vue.config.js ./
COPY .eslintrc.js ./


RUN bash bun install
COPY src ./src
CMD ["bash", "bun", "serve"]
