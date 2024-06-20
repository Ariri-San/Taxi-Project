FROM node:20.11.1-alpine3.19
# RUN addgroup app && adduser -S -G app app
# USER app

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

EXPOSE 3000 

CMD ["npm", "start", "--save-dev", "@babel/plugin-proposal-private-property-in-object", "--legacy-peer-deps"]