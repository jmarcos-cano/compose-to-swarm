# Compose on Kubernetes


https://github.com/docker/compose-on-kubernetes



```bash

# in docker desktop
kubectl api-versions | grep compose

```

## Our app

```bash
docker stack deploy --orchestrator=kubernetes -c  docker-compose.simple.yml compose_swarm_k8


kubectl get all -l "com.docker.stack.namespace=compose_swarm_k8"

```



---
## From examples


```bash
# ---------
echo """
version: '3.3'

services:

  db:
    build: db
    image: dockersamples/k8s-wordsmith-db

  words:
    build: words
    image: dockersamples/k8s-wordsmith-api
    deploy:
      replicas: 5

  web:
    build: web
    image: dockersamples/k8s-wordsmith-web
    ports:
     - "33000:80"

""" > compose/compose-k8.yaml

docker stack deploy --orchestrator=kubernetes -c  compose/compose-k8.yaml hellokube


```


### Other installations

- AKS
- EKS
- GKE
- kind
- minikube
- microk8s


# [kompose](https://github.com/kubernetes/kompose)

- only version 1,2 or 3
- [conversion matrix](https://github.com/kubernetes/kompose/blob/master/docs/conversion.md)

```bash
kompose convert -f compose/docker-compose.kompose.yml --stdout
```