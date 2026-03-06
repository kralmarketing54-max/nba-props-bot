# Frontend Dockerfile
FROM node:20-alpine

# Çalışma dizini
WORKDIR /app

# Bağımlılıkları kopyala ve yükle
COPY package.json package-lock.json* ./
RUN npm ci

# Kaynak kodları kopyala
COPY . .

# Port aç
EXPOSE 3000

# Geliştirme modunda başlat (production için değişecek)
CMD ["npm", "run", "dev"]
