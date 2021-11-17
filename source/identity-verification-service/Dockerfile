FROM node:16-alpine

LABEL environment=Production
LABEL author="Ramkumar J Damodaran"
LABEL company=IOMEGA

COPY . /app

WORKDIR /app

RUN npm install

ENTRYPOINT ["./node_modules/.bin/nodemon", "main.js"]