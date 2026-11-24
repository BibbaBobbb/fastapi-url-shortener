# URL Shortener

A REST API service for creating short links, built with **FastAPI** and **Redis**.

## Features

- Create short links with a custom slug or an auto-generated one
- Redirect by short link (`/r/{slug}`) with a visit counter
- Read, update (PUT / PATCH) and delete links
- Duplicate slug protection (`409 Conflict`)
- Input validation with Pydantic
- Interactive API docs (Swagger UI)
- Logging with configurable log level
- Tests with pytest

## Tech stack

Python 3.13 · FastAPI · Pydantic · Redis · Docker / Docker Compose · pytest · uv

## Run with Docker Compose

```shell
docker compose up -d --build
```

- API docs: http://localhost:8000/docs
- Redirect example: http://localhost:8000/r/{slug}

View logs:

```shell
docker compose logs -f
```

Stop:

```shell
docker compose down
```

## Local development

Start Redis:

```shell
docker compose up -d redis
```

Install dependencies and run the dev server:

```shell
uv sync
cd url-shortener
uv run fastapi dev
```

In PyCharm: right click `url-shortener` -> Mark Directory as -> Sources Root.

### Environment variables

| Variable     | Default     | Description    |
|--------------|-------------|----------------|
| `REDIS_HOST` | `localhost` | Redis host     |
| `REDIS_PORT` | `6379`      | Redis port     |
| `REDIS_DB`   | `0`         | Redis database |
| `LOG_LEVEL`  | `INFO`      | Logging level  |

## API

| Method | Path                         | Description                |
|--------|------------------------------|----------------------------|
| POST   | `/api/v1/short-urls/`        | Create a short link        |
| GET    | `/api/v1/short-urls/`        | List all links             |
| GET    | `/api/v1/short-urls/{slug}/` | Get link details           |
| PUT    | `/api/v1/short-urls/{slug}/` | Update a link              |
| PATCH  | `/api/v1/short-urls/{slug}/` | Partially update a link    |
| DELETE | `/api/v1/short-urls/{slug}/` | Delete a link              |
| GET    | `/r/{slug}`                  | Redirect to the target URL |

Example request:

```json
POST /api/v1/short-urls/
{
  "target_url": "https://google.com",
  "slug": "google"
}
```

If `slug` is omitted, a random 6-character slug is generated.

## Storage

Links are stored in Redis in two hashes:

- `short-urls` — slug → link data (JSON)
- `short-urls:visits` — slug → visit counter (incremented atomically with `HINCRBY`)

## Tests

Redis must be running (`docker compose up -d redis`). Tests use a separate Redis database (`15`) and don't touch real
data.

```shell
uv run pytest -v
```

## Project structure

```
url-shortener/
├── main.py              # app entry point
├── app_lifespan.py      # startup / shutdown (Redis connection)
├── core/                # config, Redis client
├── schemas/             # Pydantic models
├── api/
│   ├── redirect_views.py
│   └── api_v1/short_urls/
│       ├── crud.py          # storage logic (Redis)
│       ├── dependencies.py
│       └── views/           # endpoints
└── tests/               # pytest tests