from typing import Union
import uvicorn
from fastapi import FastAPI
import logging
import sys
from dataclasses import dataclass
from functools import lru_cache
import rich
from pydantic import BaseModel

from config import settings, DATA_DIR

app = FastAPI()


LOGGER_FILE = DATA_DIR.joinpath("mealie.log")
DATE_FORMAT = "%d-%b-%y %H:%M:%S"
LOGGER_FORMAT = "%(levelname)s: %(asctime)s \t%(message)s"
LOGGER_HANDLER = None

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@dataclass
class LoggerConfig:
    handlers: list
    format: str
    date_format: str
    logger_file: str
    level: str = logging.INFO


@lru_cache
def get_logger_config():
    if not settings.PRODUCTION:
        from rich.logging import RichHandler

        return LoggerConfig(
            handlers=[RichHandler(rich_tracebacks=True)],
            format=None,
            date_format=None,
            logger_file=None,
        )

    output_file_handler = logging.FileHandler(LOGGER_FILE)
    handler_format = logging.Formatter(LOGGER_FORMAT, datefmt=DATE_FORMAT)
    output_file_handler.setFormatter(handler_format)

    # Stdout
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(handler_format)

    return LoggerConfig(
        handlers=[output_file_handler, stdout_handler],
        format="%(levelname)s: %(asctime)s \t%(message)s",
        date_format="%d-%b-%y %H:%M:%S",
        logger_file=LOGGER_FILE,
    )


logger_config = get_logger_config()

logging.basicConfig(
    level=logger_config.level,
    format=logger_config.format,
    datefmt=logger_config.date_format,
    handlers=logger_config.handlers,
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    print(item_id)
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

def main():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        log_level="debug",
        use_colors=True,
        log_config=None,  # See Here
    )


if __name__ == "__main__":
    main()
