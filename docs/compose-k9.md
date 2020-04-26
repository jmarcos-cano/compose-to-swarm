# Compose on Kubernetes


https://github.com/docker/compose-on-kubernetes



```bash

# in docker desktop
kubectl api-versions | grep compose




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