# Stage 1 — Build the frontend
FROM node:22-alpine AS builder
WORKDIR /app

# Copy package.json & install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the project & build
COPY . .
RUN npm run build

# Stage 2 — Serve with Nginx
FROM nginx:1.27-alpine
WORKDIR /usr/share/nginx/html

# Remove default Nginx static files
RUN rm -rf ./*

# Copy built files from builder stage
COPY --from=builder /app/dist ./

# Copy a custom Nginx config (optional)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
