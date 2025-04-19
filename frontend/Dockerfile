FROM node:18-bullseye

WORKDIR /app

ENV ROLLUP_NO_BINARY=true

COPY package.json yarn.lock ./
RUN yarn install --network-timeout 100000

COPY . .

EXPOSE 5173

CMD ["yarn", "dev"]