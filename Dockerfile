# Multi-stage build
FROM node:18-alpine AS frontend-build

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install --legacy-peer-deps
COPY frontend/ ./
RUN npm run build --prod

FROM python:3.11-slim

# Install nginx for serving frontend
RUN apt-get update && apt-get install -y nginx && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy backend
COPY backend/requirements.txt ./backend/
RUN pip install -r backend/requirements.txt
COPY backend/ ./backend/

# Copy built frontend to nginx
COPY --from=frontend-build /app/frontend/dist/dynoia-frontend /var/www/html

# Configure nginx
RUN echo 'server { \
    listen 4200; \
    root /var/www/html; \
    index index.html; \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
    location /api/ { \
        proxy_pass http://localhost:8000; \
    } \
}' > /etc/nginx/sites-available/default

# Copy startup script
COPY docker-start.sh ./
RUN chmod +x docker-start.sh

# Environment variables for AWS
ENV AWS_DEFAULT_REGION=us-east-1
ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""

EXPOSE 8000 4200

CMD ["./docker-start.sh"]
