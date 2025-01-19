from fastapi import FastAPI, Path, Body, HTTPException
from pydantic import BaseModel
from typing import Annotated, List

app = FastAPI()


users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get('/users')
async def get_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def create_users(
        username: Annotated[str, Path(min_length= 5,
                                      max_length= 20,
                                      description= 'Enter username',
                                      example= 'UrbanUser')],
        age: Annotated[int, Path(ge= 18,
                                 le= 120,
                                 description= 'Enter age',
                                 example = 24)]) -> User:
    new_user = User(id= users[-1].id + 1 if len(users) > 0 else 1, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
async def update_users(user_id: Annotated[int, Path(ge= 1,
                                                   le= 100,
                                                   description ='Enter User ID',
                                                   example= 1)],
                        username: Annotated[str, Path(min_length= 5,
                                                      max_length= 20,
                                                      description= 'Enter username',
                                                      example= 'UrbanUser')],
                        age: Annotated[int, Path(ge= 18,
                                                 le= 120,
                                                 description= 'Enter age',
                                                 example = 24)]) -> User:
    try:
        user = users[user_id - 1]
        user.username = username
        user.age = age
        return user
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_users(user_id: Annotated[int, Path(ge= 1,
                                                   le= 100,
                                                   description ='Enter User ID',
                                                   example= 1)]) -> User:
    try:
        user = users[user_id - 1]
        users.pop(user_id - 1)
        return user
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')

