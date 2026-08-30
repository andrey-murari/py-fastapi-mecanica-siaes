# py-fastapi-mecanica-siaes

API FastAPI da oficina. Sobe a aplicação (`main.py`) e o MySQL pelo Docker.

## Pré-requisitos

- Docker

A imagem copia `.env.sample` para `.env`. Adaptadores vêm do env (`FOR_GET_ADDRESS`, `FOR_STORING_DATA` + `MYSQL_URL` ou `SQLITE_URL`). No Compose a app usa o host `db` na porta `3306`.

## Subir

1. Build da imagem (Dockerfile):

```bash
docker build -t mecanica:latest .
```

1. App + MySQL:

```bash
docker compose up
```

- API: [http://localhost:8000/docs](http://localhost:8000/docs)
- Admin JWT (`POST /login`): user `admin`, senha `admin` (troca depois no `.env.sample` e rebuild)
- MySQL no host: `127.0.0.1:3307` — user `root`, senha `siae-dev`, database `siae`

Para rebuild + start num comando: `docker compose up --build`.

## Seed (opcional)

```bash
docker compose exec -T db mysql -uroot -psiae-dev siae < scripts/seed_mysql.sql
```

## Parar

`Ctrl+C` no compose em foreground, ou `docker compose down`. O volume `db_data` mantém o banco.