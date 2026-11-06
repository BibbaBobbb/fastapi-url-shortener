# FastAPI URL Shortener

## Develop

### Setup

Right click `url-shortener` -> Mark Directory as -> Sources Root

### Run

Go to workdir:
```shell
cd url-shortener
```

Run dev server:
```shell
fastapi dev
```

## Docker

### Run with Docker Compose

Build and start:
```shell
docker compose up -d --build
```

The app will be available at http://localhost:8000, API docs at http://localhost:8000/docs.

Short urls are stored in `./data/short-urls.json` on the host (mounted into the container as `/data`), so data persists between container restarts.

View logs:
```shell
docker compose logs -f
```

Stop:
```shell
docker compose down
```

### Run with Docker only

```shell
docker build -t url-shortener .
docker run -p 8000:8000 \
  -e SHORT_URLS_STORAGE_FILEPATH=/data/short-urls.json \
  -v "$(pwd)/data:/data" \
  url-shortener
```
