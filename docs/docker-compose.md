
# Docker Compose
to start using this project make sure you follow up the .env.example fill it with your own variables

```bash
cp .env.example .env
```

## Build
```bash
# build and up
docker-compose -f docker-compose.yml -f docker-compose-build.yml up --build
# only build
docker-compose -f docker-compose.yml -f docker-compose-build.yml build
# push it
docker-compose -f docker-compose.yml -f docker-compose-build.yml push
```

## Start
```bash
docker-compose up
```