# io18
Google I/O 2018 extended example.

# Slides
Slides to this repo can be found [here](http://google.com)

# Docker Compose Usage
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

# Docker Swarm mode Usage

## Visualizer
```bash
docker service create \
  --name=viz \
  --publish=8080:8080/tcp \
  --constraint=node.role==manager \
  --mount=type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock \
  dockersamples/visualizer
```

## Start
```bash
docker stack deploy -c docker-compose.yml io18
```

## Status
```bash
docker service ps io18_web
```

## Scale
```bash
docker service scale io18_web=4
```