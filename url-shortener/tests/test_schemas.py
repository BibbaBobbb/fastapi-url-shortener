import pytest
from pydantic import ValidationError

from schemas.short_url import ShortUrlCreate


def test_create_without_slug():
    short_url = ShortUrlCreate(target_url="https://google.com")
    assert short_url.slug is None


def test_create_with_slug():
    short_url = ShortUrlCreate(target_url="https://google.com", slug="esther")
    assert short_url.slug == "esther"


def test_slug_too_short():
    with pytest.raises(ValidationError):
        ShortUrlCreate(target_url="https://google.com", slug="ab")


def test_invalid_url():
    with pytest.raises(ValidationError):
        ShortUrlCreate(target_url="not a url")
