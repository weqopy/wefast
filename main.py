import asyncio
from typing import Union
import uvicorn
from fastapi import FastAPI
import sys
from pydantic import BaseModel, EmailStr
from datetime import datetime


app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "price": 35.4,
                "is_offer": True,
            }
        }


@app.get("/")
async def read_root():
    await async_test()
    return {"message": f"{datetime.now()}"}


async def async_test():
    print("async_test begin")
    # await asyncio.sleep(1)
    print("async_test end")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    print(item_id)
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user


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

# nohup python3 main.py >  ./uvicorn.log 2>&1 &
