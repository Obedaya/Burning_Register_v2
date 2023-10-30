# build stage
FROM node
WORKDIR /app
COPY package.json ./
COPY bun.lockb ./
COPY babel.config.js ./
COPY jsconfig.json ./
COPY vue.config.js ./
COPY .eslintrc.js ./

RUN npm install
COPY src ./src
CMD ["npm", "run", "serve"]
