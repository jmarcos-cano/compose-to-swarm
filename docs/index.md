# From Compose to Swarm

<!-- ![1](img/portada.png) -->


---


## Meet our app


![2](img/ourapp.png)


## Architecture

> Nada fancy

![3](img/architecture.png)


---
## Setup

```PlaywithDocker tab=
#!/bin/bash
1. Go to http://play-with-docker.com sign in with your user:pass (create account if needed).
2. Click on the wrench and select either "3 Managers and 2 Workers" or "5 managers and no workers"
3. Unless instructed run all the commands on the first node.
4. Make sure to clone the repo in the swarm nodes (PWD)



git clone https://github.com/jmarcos-cano/compose-to-swarm.git
cd compose-to-swarm
```

```SwarmCloud tab=

We will use DigitalOcean to spin up a simple swarm cluster.

```

<!-- 
```AKS tab=

We will use Azuer Kubernetes Service to spin up a simple Kubernetes cluster.

``` -->