from typing import Annotated

from fastapi import Depends, APIRouter, BackgroundTasks
from starlette.responses import RedirectResponse

from schemas.short_url import ShortUrl

from .api_v1.short_urls.crud import storage
from .api_v1.short_urls.dependencies import prefetch_short_url

router = APIRouter(
    prefix="/r",
    tags=["Redirect"],
)


@router.get("/{slug}")
@router.get("/{slug}/")
def redirect_short_url(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_url),
    ],
    background_tasks: BackgroundTasks,
):
    storage.increment_visits(url)
    background_tasks.add_task(storage.save_state)
    return RedirectResponse(
        url=str(url.target_url),
    )
