FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

EXPOSE 5173

# Start Vite server, bound to all interfaces for Docker
CMD ["npm", "run", "dev", "--", "--host"]
