FROM node:20-slim as build
WORKDIR /app
COPY package.json angular.json tsconfig.json ./
COPY src ./src
RUN npm install && npm run build

FROM nginx:stable-alpine
COPY --from=build /app/dist/app /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
