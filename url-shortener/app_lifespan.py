import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.api_v1.short_urls.crud import storage
from core import config
from core.redis_client import redis_client

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    with redis_client:
        # действия до запуска приложения
        redis_client.ping()
        log.info("Connected to Redis at %s:%s", config.REDIS_HOST, config.REDIS_PORT)
        storage.init_storage_from_state()
        # ставим эту функцию на паузу на время работы приложения
        yield
    # при выходе из with соединение с Redis закроется автоматически
