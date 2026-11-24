from fastapi import (
    APIRouter,
    status,
    HTTPException,
)

from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlRead,
)

from api.api_v1.short_urls.crud import storage

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs"],
)


@router.get(
    "/",
    response_model=list[ShortUrlRead],
)
def read_short_urls_list() -> list[ShortUrl]:
    return storage.get()


@router.post(
    "/",
    response_model=ShortUrlRead,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    short_url_create: ShortUrlCreate,
) -> ShortUrl:
    if short_url_create.slug is None:
        short_url_create.slug = storage.generate_unique_slug()
    elif storage.exists(short_url_create.slug):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Short URL with slug {short_url_create.slug!r} already exists",
        )
    return storage.create(short_url_create)
