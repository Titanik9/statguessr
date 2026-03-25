FROM node:22-alpine

WORKDIR /app

COPY package.json /app/package.json
COPY tsconfig.base.json /app/tsconfig.base.json
COPY apps/web /app/apps/web
COPY packages/ts-sdk /app/packages/ts-sdk

RUN npm install
RUN npm run build --workspace @relay-console/web

CMD ["npm", "run", "start", "--workspace", "@relay-console/web", "--", "--hostname", "0.0.0.0", "--port", "3000"]
