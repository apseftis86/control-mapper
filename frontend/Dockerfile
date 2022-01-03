FROM node:lts-alpine AS build
WORKDIR /app
COPY control-map/package.json ./
RUN npm install --force
COPY control-map .
RUN npm run build
FROM nginx:stable-alpine
COPY --from=build /app/dist/control-map /var/www/html
