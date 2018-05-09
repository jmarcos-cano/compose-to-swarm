# io18
Google I/O 2018 extended example.

# Index
1. [Local Environment](#local-environment)
2. [Local Env with Docker Compose](#docker-compose-usage)
3. [Production environment with Docker swarm mode](#swarm-mode-lab)
    - Simple service create
    - scale our service
    - Simple swarm definition (stack deploy) [.simple]
    - Environment variables injection [.simple]
    - Scale our io18_web [.simple]
    - Deployment replicas [.replicas]
    - Rolling updates [.rolling]
    - Limit Host resources [.resources]
    - Healthcheck and self healing [.health]

# Slides
Slides to this repo can be found [here](http://slides.com/marcoscano/io18)

# Local Environment

### Merely docker runs
```bash
#create a local network, so that containers can see each other
docker network create mynetwork

# create the backend Redis container and attach it to the network
docker run --name redis -d --network mynetwork redis:alpine

# create the app container, expose it in a different port
docker run -p 5500:5000 -it --network mynetwork -e "REDIS_HOST=redis"  mcano/io18

# OR if you prefer local environment development supported by Docker
docker run -p 5500:5000 -it --network mynetwork -e "REDIS_HOST=redis" -v $(pwd):/code mcano/io18 sh
```

### Docker Compose
to start using this project make sure you follow up the .env.example fill it with your own variables

```bash
cp .env.example .env
```

#### Build
```bash
docker-compose -f docker-compose.yml -f docker-compose-build.yml up --build

docker-compose -f docker-compose.yml -f docker-compose-build.yml build

docker-compose -f docker-compose.yml -f docker-compose-build.yml push

```

#### Start
```bash
docker-compose up
```
# Swarm Mode lab
## 1. Enable Visualizer on port 8080
```bash
docker service create \
  --name=viz \
  --publish=8080:8080/tcp \
  --constraint=node.role==manager \
  --mount=type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock \
  dockersamples/visualizer
```

## 2. Simple service create
Create a swarm service from a Nginx docker image
```bash
docker service create --name nginx-ws -p 80:80 nginx
```
List the current services
```bash
docker service ls
```
Go to your visualizer (click in your upper link port 8080) and see how the services are spread.

## 2.1 Scale the service
```bash
docker service update --replicas 3 nginx-ws 
```


## Start
```bash
docker stack deploy -c docker-compose.yml --resolve-image=always io18
```

## Status
```bash
docker service ps io18_web
```

## Scale
```bash
docker service scale io18_web=4
```