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
docker stack deploy -c docker-compose.simple.yml --resolve-image=always --with-registry-auth intro

# list current services
docker service ls


```
<br>

> ⚠️ Go to your app (click in your upper link port 500) and see how the app looks like. !

> Go to your visualizer (click in your upper link port 8080) and see how the services are spread.

Show current status
```bash
docker service ps docker_intro_web
```

---
## 4. Environment Variables injection
> 💡 This will give you a small intro to how you can manage configuration per environment (dev,qa,stage,production)
```bash
# inspect the stack file and try to find the directive "FOO=${FOO:-BAR}"
cat docker-compose.simple.yml

# inject the new value
export FOO="Hola Edmundo"

# deploy it and see it update automatically
docker stack deploy -c docker-compose.simple.yml --resolve-image=always docker_intro
```
<br>

> 🥇 Dare you to put your own Text there, see how sometimes the application becomes unaccessible?

---
## 5. Scale web app

Want to handle more traffic?
Want to be more resilient?
Want High Availability?

Swarm got you covered

```bash
docker service scale docker_intro_web=4
```
<br>

> ⚠️ Go to your app (click in your upper link port 500) and see how which task/container responds

> Go to your visualizer (click in your upper link port 8080) and see how the services are spread.

---
## 6. Declarative Deployment Replicas
Instead of scaling your service everytime, why don't we declare it?

```bash
# Inspect the .replicas file and find "deploy: " section
cat docker-compose.replicas.yml

# Deploy new update for the stack
docker stack deploy -c docker-compose.replicas.yml --resolve-image=always docker_intro
```
> Go to your visualizer (click in your upper link port 8080) and see how the services are spread.
<br>

> 🥇 I dare you to set more than 3 replicas for docker_intro_web, how?

---
## 7. Rolling Updates
Rolling updates let you update your app with zero-downtime.
<br>

> 💡 v1 has been running for 2 weeks now and you are ready to ship your new and hottest feature on v2, with rolling updates you can easily ship v2 let it coexist with v1 until v1 gets fully drain (removed) and v2 gets out.

```bash
# inspect .rolling file and find the "update_config:" section, try to understand it
less docker-compose.rolling.yml

# Deploy/update this new configuration for your stack
docker stack deploy -c docker-compose.rolling.yml --resolve-image=always docker_intro

```
> press 'q' to exit from 'less'

#### Lets force update to see the rolling updates
Do this how many times you need in order to see it working.

```bash
# graceful full restart of your app
docker service update --force docker_intro_web
```
> Go to your visualizer (click in your upper link port 8080) and see how the services are spread.



---
## 8. Host limit resource
One can prevent memory starvation or CPU consumption of your app by adding "resources:" section

```bash
# inspect .resources file and find the "resources:" section, try to understand it
less docker-compose.resources.yml

# Deploy/update this new configuration for your stack
docker stack deploy -c docker-compose.resources.yml --resolve-image=always docker_intro

```

## 9. Health Check and Self healing
Auto restarts and health-check can also be possible by adding "healthcheck: "


```bash
# Run docker ps first to see there's no (healthy)
docker ps

# inspect .health file and find the "healthcheck:" section, try to understand it
less docker-compose.health.yml

# Deploy/update this new configuration for your stack
docker stack deploy -c docker-compose.health.yml --resolve-image=always docker_intro

# after a few seconds run
docker ps
```

Do a: `docker service ps docker_intro_web`, Identify the placement of a container (identify on which node is running).

Jump into that node and run `docker ps` find the container and its ID (first column), kill it and see how it self heals
```bash
docker kill <container ID>
```

> Go to your visualizer (click in your upper link port 8080) and see how the services are spread and self healed.

> 🥇 I dare you to do a rolling update with healthcheck included and see what happens, can you predict what will happen ahead of 'time'?


### Extra

Can you explain why this times do not match up?
```bash
docker stack deploy -c docker-compose.rolling.yml --resolve-image=always docker_intro

time docker service update --force docker_intro_web


docker stack deploy -c docker-compose.health.yml --resolve-image=always docker_intro

time docker service update --force docker_intro_web
```