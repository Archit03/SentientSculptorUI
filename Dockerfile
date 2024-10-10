# ARGs for configuration
ARG USE_CUDA=false
ARG USE_OLLAMA=false
ARG USE_CUDA_VER=cu121
ARG USE_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
ARG USE_RERANKING_MODEL=""
ARG BUILD_HASH=dev-build
ARG UID=0
ARG GID=0

# Base image for building frontend (Node.js)
FROM node:22-alpine3.20 AS build

# Set the work directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the application files
COPY . .

# Build the frontend with increased memory for Node.js
RUN NODE_OPTIONS="--max-old-space-size=4096" npm run build

# Second stage: Use a lightweight server image to serve static frontend
FROM nginx:alpine

# Set environment variables
ENV BUILD_HASH=$BUILD_HASH

# Copy the built frontend from the previous stage
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 to serve the application
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
