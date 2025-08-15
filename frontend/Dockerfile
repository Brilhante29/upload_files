FROM node:20-slim as build
WORKDIR /app
COPY package.json angular.json tsconfig.json ./
COPY src ./src
RUN npm install && npm run build

FROM node:20-slim
WORKDIR /app
COPY --from=build /app/dist/app ./dist/app
COPY server.js .
RUN npm install express
VOLUME /config
EXPOSE 80
CMD ["node", "server.js"]
