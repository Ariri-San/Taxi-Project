FROM node:20.11.1-alpine3.19
# RUN addgroup app && adduser -S -G app app
# USER app

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

EXPOSE 80

CMD ["npm", "run", "biuld"]