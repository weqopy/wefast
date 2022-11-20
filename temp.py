from rich import print
from datetime import datetime
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    id: int
    name = 'Tom'
    signup_ts: datetime | None = None
    friends: list[int] = []


eg_data = {
    'id': '123',
    'signup_ts': '2022-01-01 10:00',
    'friends': [1, 2, '3', '4']
}

user = User(**eg_data)
print(user.id)
print(repr(user.signup_ts))
print(user.friends)
print("----------------")
print(user.dict())


try:
    User(signup_ts='broken', friends=[1, 2, 'not number'])
except ValidationError as e:
    print(e.json())
