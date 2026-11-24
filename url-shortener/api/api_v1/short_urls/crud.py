"""
Create
Read
Update
Delete
"""

import logging
import secrets
import string

from core.redis_client import redis_client
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
    ShortUrlPartialUpdate,
)

log = logging.getLogger(__name__)

SLUG_ALPHABET = string.ascii_letters + string.digits
SLUG_LENGTH = 6

# Ключи в Redis:
# "short-urls"        — хеш: slug -> JSON с данными ссылки
# "short-urls:visits" — хеш: slug -> количество переходов
URLS_KEY = "short-urls"
VISITS_KEY = "short-urls:visits"


class ShortUrlsStorage:
    def _save(self, short_url: ShortUrl) -> None:
        redis_client.hset(
            URLS_KEY,
            short_url.slug,
            short_url.model_dump_json(exclude={"visits"}),
        )

    @staticmethod
    def _build(data: str, visits: str | None) -> ShortUrl:
        short_url = ShortUrl.model_validate_json(data)
        short_url.visits = int(visits or 0)
        return short_url

    def get(self) -> list[ShortUrl]:
        urls = redis_client.hgetall(URLS_KEY)
        visits = redis_client.hgetall(VISITS_KEY)
        return [self._build(data, visits.get(slug)) for slug, data in urls.items()]

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        data = redis_client.hget(URLS_KEY, slug)
        if data is None:
            return None
        return self._build(data, redis_client.hget(VISITS_KEY, slug))

    def exists(self, slug: str) -> bool:
        return bool(redis_client.hexists(URLS_KEY, slug))

    def increment_visits(self, short_url: ShortUrl) -> None:
        short_url.visits = redis_client.hincrby(VISITS_KEY, short_url.slug, 1)
        log.info("Short url %r visited %d times", short_url.slug, short_url.visits)

    def generate_unique_slug(self) -> str:
        while True:
            slug = "".join(secrets.choice(SLUG_ALPHABET) for _ in range(SLUG_LENGTH))
            if not self.exists(slug):
                return slug

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(
            **short_url_in.model_dump(),
        )
        self._save(short_url)
        log.info("Created short url %s", short_url)
        return short_url

    def delete_by_slug(self, slug: str) -> None:
        redis_client.hdel(URLS_KEY, slug)
        redis_client.hdel(VISITS_KEY, slug)
        log.info("Deleted short url %r", slug)

    def delete(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url.slug)

    def update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlUpdate,
    ) -> ShortUrl:
        for field_name, value in short_url_in:
            setattr(short_url, field_name, value)
        self._save(short_url)
        log.info("Updated short url %r", short_url.slug)
        return short_url

    def update_partial(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlPartialUpdate,
    ) -> ShortUrl:
        for field_name, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, field_name, value)
        self._save(short_url)
        log.info("Updated short url %r", short_url.slug)
        return short_url


storage = ShortUrlsStorage()
