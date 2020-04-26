
# Intro [Swarm Mode](https://docs.docker.com/engine/swarm/)
This section will give you the necessary to go full to production with Docker swarm mode.


<img src="/img/swarm.png" class="center" alt="About me" style="width:300px;">


<details>
  <summary>Swarm vs K8</summary>

<h3>Docker swarm es mejor que kubernetes .... <br> pero ustedes no estan listos para esta conversacion </h3>
<img src="/img/swarmvsk8.png" class="center" alt="About me" style="width:400px;">

- Just Kidding

</details>

<details>
  <summary>Features</summary>


<ul>
<li> Cluster management integrated with Docker Engine</li>


<li> Declarative service model </li>

<li> Scaling </li>

<li> Desired state reconciliation (The swarm manager node constantly monitors the desired state )</li>

<li> Multi-host networking </li>

<li> Service discovery </li>

<li> Load balancing</li>

<li> Secure by default (intra node) </li>

<li> Rolling updates </li>

<li> Hyper EASY </li>

</ul>
</details>


# Setup


```Local tab=
#!/bin/bash
# check swarm is enabled
docker info |grep -i swarm


docker swarm init || echo "Already in Swarm Mode"


docker node ls

```

```PlaywithDocker tab=
#!/bin/bash
1. Go to http://play-with-docker.com sign in with your user:pass (create account if needed).
2. Click on the wrench and select either "3 Managers and 2 Workers" or "5 managers and no workers"
3. Unless instructed run all the commands on the first node.
4. Make sure to clone the repo in the swarm nodes (PWD)



git clone https://github.com/jmarcos-cano/compose-to-swarm.git
cd compose-to-swarm
```

```DigitalOcean tab=
#!/bin/bash
# Create 3 droplets with private networking enabled.
# WHY 3?

# install docker
export leader=165.227.74.229
export manager1=165.227.77.199
export manager2=165.227.65.241

ssh root@${leader} "docker version || curl -fsSL https://get.docker.com/ | sh " && \
ssh root@${manager1} "docker version || curl -fsSL https://get.docker.com/ | sh" && \
ssh root@${manager2} "docker version || curl -fsSL https://get.docker.com/ | sh"


ssh root@${leader} "sudo curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-Linux-x86_64" -o /usr/bin/docker-compose &&  chmod +x /usr/bin/docker-compose" &&\
ssh root@${manager1} "sudo curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-Linux-x86_64" -o /usr/bin/docker-compose &&  chmod +x /usr/bin/docker-compose" &&\
ssh root@${manager2} "sudo curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-Linux-x86_64" -o /usr/bin/docker-compose &&  chmod +x /usr/bin/docker-compose"


# init swarm in 1 manager
#ssh root@${leader} "docker swarm init --advertise-addr eth1"

# get the manager join-token
#ssh root@${leader} "docker swarm join-token manager"


# Join the other managers


## PLUS!
docker -H ssh://root@${leader} node ls

```
