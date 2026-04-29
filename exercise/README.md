# Exercício — Orquestração com Docker Swarm

## Contexto

Você recebeu o código-fonte do sistema **Task Factory**, uma aplicação distribuída para processamento assíncrono de tarefas.

O objetivo é criar um `docker-compose.yml` compatível com Docker Swarm e gerar evidências de que a stack funcionou corretamente.

---

## Arquitetura

```text
Cliente
  |
  v
API HTTP  ---> Redis Queue ---> Workers
  |                         |
  v                         v
Viewer <---------------- Results
```

## Serviços

| Serviço | Diretório | Função |
|---|---|---|
| api | ./api | Recebe tarefas HTTP e envia para o Redis |
| worker | ./worker | Consome tarefas e processa em paralelo |
| viewer | ./viewer | Exibe status e resultados |
| redis | imagem oficial | Fila e armazenamento temporário |

---

## Sua tarefa

Crie um arquivo `docker-compose.yml` que use Docker Swarm com:

- serviço `api`
- serviço `worker`
- serviço `viewer`
- serviço `redis`
- redes overlay separadas
- réplicas
- limits de CPU/memória
- boas práticas de segurança
- evidências com comandos Docker

---

## Requisitos obrigatórios

### Imagens

O Swarm não executa `build:` com `docker stack deploy`.

Construa as imagens antes:

```bash
docker build -t task-factory-api:1.0.0 ./api
docker build -t task-factory-worker:1.0.0 ./worker
docker build -t task-factory-viewer:1.0.0 ./viewer
```

No Compose, use `image:`.

### Redes

Crie duas redes overlay:

- `frontend_net`
- `backend_net`

Regras:

- `api`: `frontend_net` e `backend_net`
- `viewer`: `frontend_net` e `backend_net`
- `worker`: somente `backend_net`
- `redis`: somente `backend_net`

### Portas

- `api`: publicar `5000:5000`
- `viewer`: publicar `5001:5001`
- `redis`: não publicar porta

### Réplicas mínimas

- `api`: 2
- `worker`: 3
- `viewer`: 1
- `redis`: 1

### Recursos

Todos os serviços devem usar `deploy.resources`.

Exemplo:

```yaml
deploy:
  resources:
    limits:
      cpus: "0.25"
      memory: 128M
```

### Segurança

Aplique nos serviços Python, quando compatível:

```yaml
user: "1000"
read_only: true
tmpfs:
  - /tmp
cap_drop:
  - ALL
security_opt:
  - no-new-privileges:true
```

---

## Inicializar Swarm

```bash
docker swarm init
docker node ls
```

---

## Deploy

```bash
docker stack deploy -c docker-compose.yml taskfactory
```

Verifique:

```bash
docker stack ls
docker service ls
docker service ps taskfactory_api
docker service ps taskfactory_worker
```

---

## Testes funcionais

### Enviar tarefas

Linux/macOS/WSL:

```bash
for i in {1..20}; do
  curl -X POST http://localhost:5000/task \
    -H "Content-Type: application/json" \
    -d "{\"value\": $i}"
  echo
done
```

PowerShell:

```powershell
1..20 | ForEach-Object {
  Invoke-RestMethod -Method Post -Uri http://localhost:5000/task `
    -ContentType "application/json" `
    -Body "{""value"": $_}"
}
```

### Ver resultados

```bash
curl http://localhost:5001/results
curl http://localhost:5001/status
```

---

## Evidências obrigatórias

Inclua no relatório:

### 1. Stack e serviços

```bash
docker stack ls
docker service ls
```

### 2. Desired state

```bash
docker service ps taskfactory_api
docker service ps taskfactory_worker
```

### 3. Load balancing

```bash
for i in {1..10}; do curl http://localhost:5000/health; echo; done
```

Evidência esperada: respostas com hostnames diferentes.

### 4. Scaling

```bash
docker service scale taskfactory_worker=5
docker service ps taskfactory_worker
```

### 5. Auto-healing

```bash
docker ps
docker kill <container_id_do_worker>
docker service ps taskfactory_worker
```

### 6. Resources limit

```bash
docker inspect <container_id>
```

Procure:

```json
"Memory": != 0,
"NanoCpus": != 0
```

### 7. Logs

```bash
docker service logs taskfactory_worker
docker service logs taskfactory_api
```

---

## Perguntas obrigatórias

1. Qual é a diferença entre `docker compose up` e `docker stack deploy`?
2. Por que o Swarm não aceita `build:` no deploy da stack?
3. O que é desired state?
4. O que aconteceu quando você matou um container?
5. Como você comprovou o load balancing?
6. Onde os limites de CPU e memória aparecem no `docker inspect`?
7. Por que o Redis não deve ser exposto diretamente?

---

## Remover a stack

```bash
docker stack rm taskfactory
```

---
