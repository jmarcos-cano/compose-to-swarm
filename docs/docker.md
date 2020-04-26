# Local Environment

### If we wanted to run it just with docker


```bash
docker run -d --rm --name -p 7777:80 web_server nginx


open http://localhost:7777



docker run -it --rm --name container1 alpine sh

```


---

### Merely docker runs
```bash
#create a local network, so that containers can see each other
docker network create mynetwork

# create the backend Redis container and attach it to the network
docker run --name redis -d --network mynetwork redis:alpine

# create the app container, expose it in a different port
docker run -p 5500:5000 -it --network mynetwork -e "REDIS_HOST=redis"  mcano/docker:intro

# OR if you prefer local environment development supported by Docker
docker run -p 5500:5000 -it --network mynetwork -e "REDIS_HOST=redis" -v $(pwd):/code mcano/docker:intro sh
```