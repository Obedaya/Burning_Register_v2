# build stage
FROM alpine
WORKDIR /app
ADD https://github.com/oven-sh/bun/releases/latest/download/bun-linux-x64.zip bun-linux-x64.zip
RUN unzip bun-linux-x64.zip
RUN mv bun-linux-x64/bun /usr/local/bin/bun 
RUN chmod +x /usr/local/bin/bun
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
