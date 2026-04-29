# Docker Swarm Lab — Versão com Falhas para Debug

Este laboratório foi criado para exercitar Docker Swarm com foco em:

- deploy de stack
- desired state
- scaling
- auto-healing
- load balancing
- limits com `deploy.resources`
- troubleshooting com `docker service ps`, `docker logs`, `docker inspect`

## Arquivos

| Arquivo | Finalidade |
|---|---|
| `docker-compose.broken.yml` | Falha de rede proposital: `web` e `api` estão em redes diferentes |
| `docker-compose.broken-image.yml` | Falha de imagem proposital: imagem da API inexistente |
| `docker-compose.broken-resources.yml` | Falha de boas práticas: serviços sem limites de recursos |
| `docker-compose.correct.yml` | Versão corrigida |
| `api/` | Código Flask usado na imagem da API |

---

# Preparação

## 1. Inicializar Swarm

```bash
docker swarm init
```

Se o Swarm já estiver ativo, siga em frente.

## 2. Construir a imagem da API

Importante: `docker stack deploy` não faz build local automaticamente.

```bash
docker build -t swarm-lab-api:1.0.0 ./api
```

---

# Parte 1 — Falha de rede

## 1. Subir a stack quebrada

```bash
docker stack deploy -c docker-compose.broken.yml lab
```

## 2. Verificar serviços

```bash
docker service ls
docker service ps lab_api
docker service ps lab_web
```

## 3. Testar acesso

```bash
curl localhost:8080
```

Resultado esperado:

- o Nginx responde erro, normalmente `502 Bad Gateway` ou página padrão sem alcançar a API

## 4. Diagnóstico esperado

Inspecione as redes:

```bash
docker network ls
docker service inspect lab_web
docker service inspect lab_api
```

Problema:

- `api` está na rede `backend`
- `web` está na rede `frontend`
- os serviços não conseguem se comunicar

## 5. Corrigir

Remova a stack:

```bash
docker stack rm lab
```

Aguarde alguns segundos e aplique a versão correta:

```bash
docker stack deploy -c docker-compose.correct.yml lab
```

---

# Parte 2 — Load balancing

Após aplicar a versão correta:

```bash
curl localhost:8080
```

Para testar várias vezes:

```bash
for i in {1..10}; do curl localhost:8080; echo; done
```

No PowerShell:

```powershell
1..10 | ForEach-Object { curl http://localhost:8080 }
```

Objetivo:

- observar respostas vindas das réplicas da API

---

# Parte 3 — Scaling

## Escalar API

```bash
docker service scale lab_api=5
```

Validar:

```bash
docker service ps lab_api
```

O Swarm deve manter 5 réplicas.

---

# Parte 4 — Auto-healing

## 1. Listar containers

```bash
docker ps
```

## 2. Matar um container da API

```bash
docker kill <container_id>
```

## 3. Validar recuperação

```bash
docker service ps lab_api
docker ps
```

Resultado esperado:

- Swarm recria automaticamente outra réplica
- desired state permanece em 5 réplicas

---

# Parte 5 — Falha de imagem

## 1. Remover stack atual

```bash
docker stack rm lab
```

## 2. Subir stack com imagem inexistente

```bash
docker stack deploy -c docker-compose.broken-image.yml lab
```

## 3. Diagnosticar

```bash
docker service ps lab_api
```

Resultado esperado:

- tasks rejeitadas ou falhando por imagem não encontrada

Ponto didático:

- o Swarm tenta alcançar o estado desejado
- mas falha porque a imagem não existe

Corrigir:

```bash
docker stack rm lab
docker stack deploy -c docker-compose.correct.yml lab
```

---

# Parte 6 — Falha de boas práticas: recursos ausentes

## 1. Subir stack sem limits

```bash
docker stack rm lab
docker stack deploy -c docker-compose.broken-resources.yml lab
```

## 2. Inspecionar container

```bash
docker ps
docker inspect <container_id>
```

Procure:

```json
"Memory": 0,
"NanoCpus": 0
```

Interpretação:

- sem limites aplicados
- risco de consumo indevido de recursos

## 3. Corrigir

```bash
docker stack rm lab
docker stack deploy -c docker-compose.correct.yml lab
```

Inspecione novamente e valide:

```json
"Memory": != 0,
"NanoCpus": != 0
```

---

# Checklist de aprendizagem

Ao final, o aluno deve explicar:

1. Por que `docker stack deploy` exige imagem já construída?
2. Como identificar erro de rede entre serviços?
3. Como o Swarm mantém o desired state?
4. O que acontece quando uma imagem não existe?
5. Como provar que limites de recursos foram aplicados?
6. Qual a diferença entre falha de container e falha de configuração?

---

# Encerramento

A principal lição deste laboratório:

> Em Swarm, o sistema tenta manter o estado desejado.  
> Mas se a declaração estiver errada, ele vai tentar manter o erro também.
