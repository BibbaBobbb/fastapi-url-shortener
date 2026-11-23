from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException,
)

from api.api_v1.short_urls.dependencies import save_storage_state
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlRead,
)

from api.api_v1.short_urls.crud import storage

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs"],
    dependencies=[Depends(save_storage_state)],
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
    if storage.get_by_slug(short_url_create.slug):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Short URL with slug {short_url_create.slug!r} already exists",
        )
    return storage.create(short_url_create)
