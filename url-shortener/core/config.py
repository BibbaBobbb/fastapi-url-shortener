import logging
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# Путь к файлу хранилища можно переопределить через переменную окружения
# (например, в Docker — на файл в смонтированном volume).
SHORT_URLS_STORAGE_FILEPATH = Path(
    os.getenv(
        "SHORT_URLS_STORAGE_FILEPATH",
        BASE_DIR / "short-urls.json",
    )
)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
