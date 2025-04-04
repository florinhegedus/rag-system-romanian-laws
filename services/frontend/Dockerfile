FROM node:18-alpine AS builder
WORKDIR /app
COPY ./services/frontend/package*.json ./
RUN npm install
COPY ./services/frontend .
RUN npm run build

FROM nginx:alpine
# Changed from /app/build to /app/build (or your configured distDir)
COPY --from=builder /app/build /usr/share/nginx/html
COPY ./services/frontend/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]