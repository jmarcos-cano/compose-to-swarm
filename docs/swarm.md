# Swarm Steps

## 0. git clone

```bash

git clone https://github.com/jmarcos-cano/compose-to-swarm.git
cd compose-to-swarm

```

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

??? info "⚠️"
    go to your visualizer (click in your upper link port 8080) and see how the services are spread.

---

## 2. Simple service create


```bash
# Create a swarm service from a Nginx docker image
docker service create --name nginx-ws -p 80:80 nginx

# List the current services
docker service ls
```


??? info "⚠️"
    Go to your visualizer (click in your upper link port 8080) and see how the services are spread.
    Click also on Port 80 (Nginx) - it should say "Welcome to Nginx"



**Scale the service**
```bash
docker service update --replicas 3 nginx-ws
```
> Go to your visualizer (click in your upper link port 8080) and see how the services are spread.

**Checking service logs**
```bash
docker service logs nginx-ws
```

**Delete the service**
```bash
docker service rm nginx-ws

# check for running services
docker service ls
```

---
## 3. Simple Stack deploy



```bash
# inspect the stack file and try to understand it
cat docker-compose.simple.yml
# deploy it
docker stack deploy -c docker-compose.simple.yml --resolve-image=always --with-registry-auth compose_swarm

# list current services
docker service ls


```
<br>

??? info "⚠️"
    Go to your app (click in your upper link port 500) and see how the app looks like. !
    Go to your visualizer (click in your upper link port 8080) and see how the services are spread.



Show current status
```bash
docker stack ps compose_swarm
```

---
## 4. Environment Variables injection
> 💡 This will give you a small intro to how you can manage configuration per environment (dev,qa,stage,production)


```bash
# inspect the stack file and try to find the directive "FOO=${FOO:-BAR}"
cat docker-compose.simple.yml

# inject the new value
export FOO="Development"

# deploy it and see it update automatically
docker stack deploy -c docker-compose.simple.yml --resolve-image=always --with-registry-auth compose_swarm

docker stack services compose_swarm

```

```bash
# PROD
docker stack deploy -c <(docker-compose --env-file .configs/production.env -f docker-compose.simple.yml config ) --resolve-image=always --with-registry-auth compose_swarm_prod

```


<br>

??? info "🥇"
    Dare you to put your own Text there, see how sometimes the application becomes unaccessible?

---
## 5. Scale web app

- Want to handle more traffic?
- Want to be more resilient?
- Want High Availability?

Swarm got you covered

```bash
docker service scale compose_swarm_web=4
```
<br>

??? info "⚠️"
    Go to your app (click in your upper link port 500) and see how which task/container responds
    Go to your visualizer (click in your upper link port 8080) and see how the services are spread.

---
## 6. Declarative Deployment Replicas
Instead of scaling your service everytime, why don't we declare it?

```bash
# Inspect the .replicas file and find "deploy: " section
cat compose/docker-compose.replicas.yml

# Deploy new update for the stack
DEPLOYMENT_REPLICAS=7 docker stack deploy -c compose/docker-compose.replicas.yml --resolve-image=always compose_swarm
```

??? info "⚠️"
    Go to your visualizer (click in your upper link port 8080) and see how the services are spread.

---
## 7. Rolling Updates
Rolling updates let you update your app with zero-downtime.
<br>

> 💡 v1 has been running for 2 weeks now and you are ready to ship your new and hottest feature on v2, with rolling updates you can easily ship v2 let it coexist with v1 until v1 gets fully drain (removed) and v2 gets out.

```bash
# inspect .rolling file and find the "update_config:" section, try to understand it
less compose/docker-compose.rolling.yml


# Deploy/update this new configuration for your stack
docker stack deploy -c <(docker-compose -f compose/docker-compose.rolling.yml config) --resolve-image=always compose_swarm

# update image
docker stack deploy -c <(IMAGE_NAME=mcano/compose-to-swarm:v2 docker-compose -f compose/docker-compose.rolling.yml config) --resolve-image=always compose_swarm
```


#### Lets force update to see the rolling updates

Do this how many times you need in order to see it working.

```bash
# graceful full restart of your app
docker service update --force compose_swarm_web
```

> Go to your visualizer (click in your upper link port 8080) and see how the services are spread.



---
## 8. Host limit resource

One can prevent memory starvation or CPU consumption of your app by adding "resources:" section

```bash
# inspect .resources file and find the "resources:" section, try to understand it
less compose/docker-compose.resources.yml

# Deploy/update this new configuration for your stack
docker stack deploy -c compose/docker-compose.resources.yml --resolve-image=always compose_swarm

```

## 9. Health Check and Self healing
Auto restarts and health-check can also be possible by adding "healthcheck: "


```bash
# Run docker ps first to see there's no (healthy)
docker ps

# inspect .health file and find the "healthcheck:" section, try to understand it
less compose/docker-compose.health.yml

# Deploy/update this new configuration for your stack
docker stack deploy -c compose/docker-compose.health.yml --resolve-image=always compose_swarm

# after a few seconds run
docker ps
```

Do a: `docker service ps compose_swarm_web`, Identify the placement of a container (identify on which node is running).

Jump into that node and run `docker ps` find the container and its ID (first column), kill it and see how it self heals
```bash
docker kill <container ID>
```

??? info "info"
    Go to your visualizer (click in your upper link port 8080) and see how the services are spread and self healed.



## Full Production + [LB](http://138-197-49-123.nip.io/make)
```
docker stack deploy -c <(docker-compose --env-file .configs/production.env -f docker-compose.yml config ) --resolve-image=always --with-registry-auth compose_swarm_prod

open http://138-197-49-123.nip.io/

```