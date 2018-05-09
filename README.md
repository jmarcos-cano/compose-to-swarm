# io18
Google I/O 2018 extended example.

## Before you start

1. Go to [http://play-with-docker.com](http://play-with-docker.com) sign in with the user:pass provided in the presentation.
2. Click on the wrench and select either "3 Managers and 2 Workers" or "5 managers and no workers"


# Index
1. [Local Environment](#local-environment)
2. [Local Env with Docker Compose](#docker-compose-usage)
3. [Docker Swarm Mode - Lab](#swarm-mode-lab)
    - [Simple service create](#2-simple-service-create)
    - Scale the service
    - [Simple swarm definition (stack deploy)](#3-simple-stack-deploy)
    - [Environment variables injection](#4-environment-variables-injection)
    - [Scale our io18_web](#5-scale-web-app)
    - [Declarative deployment replicas](#6-declarative-deployment-replicas)
    - [Rolling updates](#7-rolling-updates)
    - [Limit Host resources](#8-host-limit-resource)
    - [Healthcheck and self healing](#9-health-check-and-self-healing)

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
# build and up
docker-compose -f docker-compose.yml -f docker-compose-build.yml up --build
# only build
docker-compose -f docker-compose.yml -f docker-compose-build.yml build
# push it
docker-compose -f docker-compose.yml -f docker-compose-build.yml push
```

#### Start
```bash
docker-compose up
```
---

# Swarm Mode lab
This section will give you the necessary to go full to production with Docker swarm mode.

## 1. Enable Visualizer on port 8080
```bash
docker service create \
  --name=viz \
  --publish=8080:8080/tcp \
  --constraint=node.role==manager \
  --mount=type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock \
  dockersamples/visualizer

# wait until it says "service converged"
```
>  go to your visualizer (click in your upper link port 8080) and see how the services are spread.

---
## 2. Simple service create
```bash
# Create a swarm service from a Nginx docker image
docker service create --name nginx-ws -p 80:80 nginx

# List the current services
docker service ls
```
> Go to your visualizer (click in your upper link port 8080) and see how the services are spread.

> Click also on Port 80 (Nginx) - it should say "Welcome to Nginx"

**Scale the service**
```bash
docker service update --replicas 3 nginx-ws
```
> Go to your visualizer (click in your upper link port 8080) and see how the services are spread.

**Delete the service**
```bash
docker service rm nginx-ws

# check for running services
docker service ls
```

---
## 3. Simple Stack deploy

Make sure to clone the repo
```bash
git clone https://github.com/jmarcos-cano/io18.git
cd io18
```

```bash
# inspect the stack file and try to understand it
cat docker-compose.simple.yml
# deploy it
docker stack deploy -c docker-compose.simple.yml --resolve-image=always io18

# list current services
docker service ls


```


> Go to your visualizer (click in your upper link port 8080) and see how the services are spread.



Show current status
```bash
docker service ps io18_web
```

---
## 4. Environment Variables injection
> This will give you a small intro to how you can manage configuration per environment (dev,qa,stage,production)
```bash
# inspect the stack file and try to find the directive "FOO=${FOO:-BAR}"
cat docker-compose.simple.yml

# inject the new value
export FOO="Hello io18"

# deploy it and see it update automatically
docker stack deploy -c docker-compose.simple.yml --resolve-image=always io18
```

---
## 5. Scale web app
```bash
docker service scale io18_web=4
```
> Go to your visualizer (click in your upper link port 8080) and see how the services are spread.

---
## 6. Declarative Deployment Replicas
```bash
# Inspect the .replicas file and find "deploy: " section
cat docker-compose.replicas.yml

# Deploy new update for the stack
docker stack deploy -c docker-compose.replicas.yml --resolve-image=always io18
```
> Go to your visualizer (click in your upper link port 8080) and see how the services are spread.

I dare you to set more than 3 replicas for io18_web, how?

---
## 7. Rolling Updates
Rolling updates let you update your app with zero-downtime.

> v1 has been running for 2 weeks now and you are ready to ship your new and hottest feature on v2, with rolling updates you can easily ship v2 let it coexist with v1 until v1 gets fully drain (removed) and v2 gets out.

```bash
# inspect .rolling file and find the "update_config:" section, try to understand it
less docker-compose.rolling.yml

# Deploy/update this new configuration for your stack
docker stack deploy -c docker-compose.rolling.yml --resolve-image=always io18

```
> press 'q' to exit from 'less'

#### Lets force update to see the rolling updates

```bash
# graceful full restart of your app
docker service update --force io18_web
```
> Go to your visualizer (click in your upper link port 8080) and see how the services are spread.

---
## 8. Host limit resource
One can prevent memory starvation or CPU consumption of your app by adding "resources:" section

```bash
# inspect .resources file and find the "resources:" section, try to understand it
less docker-compose.resources.yml

# Deploy/update this new configuration for your stack
docker stack deploy -c docker-compose.resources.yml --resolve-image=always io18

```

## 9. Health Check and Self healing
Auto restarts and health-check can also be possible by adding "healthcheck: "

```bash
# inspect .health file and find the "healthcheck:" section, try to understand it
less docker-compose.health.yml

# Deploy/update this new configuration for your stack
docker stack deploy -c docker-compose.health.yml --resolve-image=always io18
```

Do a: `docker service ps io18_web`, Identify the placement of a container (identify on which node is running).

Jump into that node and run `docker ps` find the container and its ID (first column), kill it and see how it self heals
```bash
docker kill <container ID>
```

> Go to your visualizer (click in your upper link port 8080) and see how the services are spread and self healed.
