import asyncio
from typing import Union
import uvicorn
from fastapi import FastAPI, status, Form
import sys
from pydantic import BaseModel, EmailStr
from datetime import datetime


app = FastAPI()


@app.get("/", status_code=200)
async def root():
    await async_test()
    return {"message": f"{datetime.now()}"}


async def async_test():
    asyncio.sleep(1)


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
