# io18
Google I/O 2018 extended example.

# Index
1. [Local Environment](#local-environment)
2. [Local Env with Docker Compose](#docker-compose-usage)
3. [Production environment with Docker swarm mode (Lab)](#swarm-mode-lab)
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
## 1. Enable Visualizer on port 8080
```bash
docker service create \
  --name=viz \
  --publish=8080:8080/tcp \
  --constraint=node.role==manager \
  --mount=type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock \
  dockersamples/visualizer
```
> Go to your visualizer (click in your upper link port 8080) and see how the services are spread.

---
## 2. Simple service create
```bash
# Create a swarm service from a Nginx docker image
docker service create --name nginx-ws -p 80:80 nginx

# List the current services
docker service ls
```
> Go to your visualizer (click in your upper link port 8080) and see how the services are spread.

**Scale the service**
```bash
docker service update --replicas 3 nginx-ws 
```
> Go to your visualizer (click in your upper link port 8080) and see how the services are spread.

---
## 3. Simple Stack deploy
```bash
# inspect the stack file and try to understand it
cat docker-compose.simple.yml
# deploy it
docker stack deploy -c docker-compose.simple.yml --resolve-image=always io18
```

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
## 6. Deployment Replicas declarative
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
