# Portal-UI Vue.js multi-stage build
# Build context: supplier-portal-ui directory
# Requires: nginx.conf in the build context (copy from docker/portal-ui/)
FROM node:20-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
# Skip prebuild (type generation requires Frappe backend)
# Types should be pre-generated before building the image
RUN npm run build --ignore-scripts || (vue-tsc -b && npx vite build)

FROM nginx:alpine AS production

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
