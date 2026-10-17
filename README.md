# py-fastapi-mecanica-siaes

API FastAPI da oficina. Sobe a aplicação (`main.py`) e o MySQL pelo Docker Compose ou pelo Kubernetes (minikube).

A aplicação lê a configuração do ambiente: adaptador de endereço (`FOR_GET_ADDRESS`), banco (`FOR_STORING_DATA`, `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`) e JWT (`JWT_SECRET`, `ADMIN_LOGIN`, `ADMIN_PASSWORD`). A referência local está em `.env.sample`.

## Pré-requisitos

- Docker
- Para o cluster local: [minikube](https://minikube.sigs.k8s.io/docs/start/) e `kubectl`

## Docker Compose

```bash
docker compose up --build
```

- API: [http://localhost:8000/docs](http://localhost:8000/docs)
- Admin JWT (`POST /login`): user `admin`, senha `admin` (valores de `.env.sample`)
- MySQL no host: `127.0.0.1:3307` — user `root`, senha `siae-dev`, database `siae`

No Compose o serviço da API aponta o MySQL para o host `db` na porta `3306`.

Seed opcional:

```bash
docker compose exec -T db mysql -uroot -psiae-dev siae < scripts/seed_mysql.sql
```

Para parar: `Ctrl+C` no Compose em foreground, ou `docker compose down`. O volume `db_data` mantém o banco.

## Kubernetes (minikube)

Os manifests ficam em `k8s/`:

| Arquivo | O que sobe |
| --- | --- |
| `configmap.yaml` | ConfigMaps `api-config` e `db-config` |
| `services.yaml` | `mecanica-api-svc` (NodePort `30100`) e `mecanica-mysql-svc` (ClusterIP) |
| `deployments.yaml` | Deployment da API (3 réplicas) e do MySQL (1 réplica) |

A API usa a imagem `andreymurari/mecanica-siaes:2.0.0`. O Deployment sobrescreve `MYSQL_HOST` para o Service `mecanica-mysql-svc`. Usuário, senha e database vêm do `db-config` (`siae` / `siae` / `siae`).

### Subir

```bash
minikube start
kubectl apply -f k8s/configmap.yaml -f k8s/services.yaml -f k8s/deployments.yaml
kubectl get pods -w
```

Espere `mecanica-mysql-...` e os pods `mecanica-api-...` em `Running` com `READY 1/1`. A API só inicia depois que o MySQL aceita conexão na porta `3306`.

### Testar

O NodePort não responde em `localhost`. Peça a URL ao minikube:

```bash
minikube service mecanica-api-svc --url
```

A saída é o endereço do nó, no formato `http://<ip-do-minikube>:30100`. A documentação da API fica em:

`http://<ip-do-minikube>:30100/docs`

Para abrir no navegador:

```bash
minikube service mecanica-api-svc
```

Login admin neste cluster: user `admin`, senha `change-me` (`k8s/configmap.yaml`).

Se o IP do minikube não responder na máquina (comum com o driver Docker no Windows), publique o Service localmente:

```bash
kubectl port-forward svc/mecanica-api-svc 8000:80
```

Aí o teste é [http://localhost:8000/docs](http://localhost:8000/docs).

### Parar

```bash
kubectl delete -f k8s/deployments.yaml -f k8s/services.yaml -f k8s/configmap.yaml
minikube stop
```
