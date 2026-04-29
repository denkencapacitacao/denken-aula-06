
# Docker Swarm Lab

## Setup

````bash
docker swarm init
docker stack deploy -c docker-compose.yml lab
````

## Test
````bash
curl localhost:8080
````

## Scale
````bash
docker service scale lab_api=5
````

## Auto-healing
````bash
docker ps
docker kill <container_id>
````

## Inspect
````bash
docker inspect <container_id>
````