# Build the app
FROM node:20-slim AS builder

WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Copy the rest and build
COPY . .
RUN npm run build

# Production server
FROM node:20-slim AS production

WORKDIR /app

# Install only `vite` for serving 
RUN npm install -g vite

# Copy built files from the builder stage
COPY --from=builder /app/dist /app/dist
COPY --from=builder /app/node_modules ./node_modules

# Expose port 
EXPOSE 4173

# Run Vite's production preview server
CMD ["vite", "preview", "--host", "0.0.0.0"]