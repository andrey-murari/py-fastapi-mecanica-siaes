# py-fastapi-mecanica-siaes

API FastAPI da oficina. Em produção roda no EKS e usa o MySQL do RDS. Os dois nascem no Terraform, em `infra/`. O deploy dos manifests fica em `k8s/overlays/production` e também no workflow `Deploy to Kubernetes`.

A aplicação lê o ambiente: `FOR_GET_ADDRESS`, `FOR_STORING_DATA`, `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`, `JWT_SECRET`, `ADMIN_LOGIN` e `ADMIN_PASSWORD`.

## Pré-requisitos

- Terraform `>= 1.10`
- AWS CLI e `kubectl`
- Credenciais do AWS Academy Learner Lab em `us-east-1` (access key, secret e session token)
- As roles do lab cujo nome contém `LabEksClusterRole` e `LabEksNodeRole`
- Docker, se for subir a API na máquina

## Do Terraform até o teste no pod

### 1. Credenciais

No terminal do lab, exporte a access key, a secret e o session token. A região é `us-east-1`.

```bash
aws sts get-caller-identity
```

### 2. Senha do RDS

Crie `infra/terraform.tfvars` (esse arquivo não entra no Git):

```hcl
mysql_password = "uma-senha-de-8-a-41"
```

A senha tem de 8 a 41 caracteres, sem espaço, aspas, barra ou `@`. O usuário do banco é `siae`. O RDS não aceita `root`.

### 3. Bucket do state

O state fica no S3, no bucket declarado em `infra/backend.tf`. Se esse bucket ainda não existir:

```bash
terraform -chdir=infra/bootstrap init
terraform -chdir=infra/bootstrap apply
```

### 4. Criar EKS, RDS e ECR

```bash
terraform -chdir=infra init
terraform -chdir=infra apply
```

O apply cria o cluster `mecanica-siaes` (Kubernetes 1.35, um nó `t3.small`), o RDS MySQL 8.0 público e o repositório ECR `fiap-17soat/siaes-ci-cd`. A porta 30100 do nó fica aberta para o teste da API. O EKS consome crédito do lab enquanto existir.

Confira os endereços:

```bash
terraform -chdir=infra output
```

`mysql_host` é o endpoint do RDS, sem porta e sem aspas. `ecr_repository_url` é o registry da imagem.

### 5. Imagem no ECR

A imagem precisa existir nesse repositório antes do pod subir. O workflow `CI Multistage Pipeline` publica a imagem no push para `main`. O workflow `Deploy to Kubernetes` roda em seguida, nesse branch, ou por `workflow_dispatch`.

Secrets do repositório usadas nesse deploy:

| Secret | Valor |
| --- | --- |
| `AWS_ACCESS_KEY_ID` | Access key do lab |
| `AWS_SECRET_ACCESS_KEY` | Secret key do lab |
| `AWS_SESSION_TOKEN` | Session token do lab |
| `MYSQL_HOST` | Saída `mysql_host`, só o hostname |
| `MYSQL_PASSWORD` | A mesma senha de `infra/terraform.tfvars` |

### 6. Subir os manifests na mão

Use o mesmo usuário IAM que rodou o Terraform.

```bash
aws eks update-kubeconfig --region us-east-1 --name mecanica-siaes

MYSQL_HOST="$(terraform -chdir=infra output -raw mysql_host)"
read -s MYSQL_PASSWORD
printf '\n'

kubectl create secret generic prod-db-secret \
  --from-literal=MYSQL_HOST="$MYSQL_HOST" \
  --from-literal=MYSQL_PASSWORD="$MYSQL_PASSWORD" \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl apply -k k8s/overlays/production
kubectl rollout status deployment/prod-mecanica-siaes --timeout=300s
kubectl get pods -l app=mecanica-siaes
```

O pod `prod-mecanica-siaes` fica `Running` e `1/1`. O `initContainer` espera o RDS aceitar TCP na porta 3306. `MYSQL_HOST` e `MYSQL_PASSWORD` vêm da Secret `prod-db-secret`. Usuário e database (`siae` / `siae`) vêm do ConfigMap. O login admin é `admin` / `change-me`.

O HPA permite de 1 a 3 réplicas, com alvo de 70% de CPU. Sem o metrics-server no cluster, o alvo permanece `unknown` e o número de réplicas não muda.

### 7. Chamar o endpoint

O Service é NodePort `30100`. O IP público não sai no `terraform output`. Pegue a coluna `EXTERNAL-IP`:

```bash
kubectl get nodes -o wide
```

```bash
NODE_IP="$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="ExternalIP")].address}')"

curl -sS -X POST "http://${NODE_IP}:30100/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"login":"admin","password":"change-me"}'
```

A resposta traz `access_token` e `token_type`. A documentação fica em `http://<EXTERNAL-IP>:30100/docs`. No Postman, o método é POST e o corpo é JSON.

### 8. Derrubar

```bash
terraform -chdir=infra destroy
```

## Docker Compose

Sobe a API e um MySQL local, sem usar o RDS.

```bash
docker compose up --build
```

- API: [http://localhost:8000/docs](http://localhost:8000/docs)
- Login: `POST /auth/login` com `admin` / `change-me`
- MySQL no host: `127.0.0.1:3307`, database `siae`, usuário `siae`, senha `siae`. O root local é `siae-dev`.

Dentro do Compose a API fala com o host `db` na porta `3306`.

Seed opcional:

```bash
docker compose exec -T db mysql -uroot -psiae-dev siae < scripts/seed_mysql.sql
```

Para parar: `Ctrl+C`, ou `docker compose down`. O volume `db_data` mantém o banco.
