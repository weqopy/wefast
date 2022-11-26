import asyncio
from typing import Union
import uvicorn
from fastapi import FastAPI
import sys
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
async def read_root():
    await async_test()
    return {"message": "Hello World"}

async def async_test():
    print("async_test begin")
    await asyncio.sleep(1)
    print("async_test end")

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    print(item_id)
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


def main():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_delay=0.3,
    )


if __name__ == "__main__":
    main()
