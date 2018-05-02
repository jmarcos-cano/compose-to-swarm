# io18-compose-example
Google I/O 2018 extended example.


# Usage
to start using this project make sure you follow up the .env.example fill it with your own variables

```bash
cp .env.example .env
```

## Build
```bash
docker-compose -f docker-compose.yml -f docker-compose-build.yml build

docker-compose -f docker-compose.yml -f docker-compose-build.yml push

```

## Start
```bash
docker-compose up
```