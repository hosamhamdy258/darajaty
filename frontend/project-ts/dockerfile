FROM node:20.11.0-slim

WORKDIR /app

# Copy both package.json and package-lock.json to leverage Docker cache
COPY package*.json ./

RUN npm install

COPY . .

# # Build the Vite project
# RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "dev"]
