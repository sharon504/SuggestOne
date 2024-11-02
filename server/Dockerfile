FROM node

WORKDIR /usr/src/app/server

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

COPY ./package.json ./

RUN pnpm i 

EXPOSE 2000
