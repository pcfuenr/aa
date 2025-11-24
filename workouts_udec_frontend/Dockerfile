FROM node:20-alpine AS rico

WORKDIR /workouts_udec_frontend
COPY package*.json ./

#Instalar dependencias
RUN npm install

COPY . .
RUN npm run build

#Imagen lista
FROM nginxinc/nginx-unprivileged:stable-alpine

COPY --from=rico /workouts_udec_frontend/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 4173
CMD ["nginx", "-g", "daemon off;"]
