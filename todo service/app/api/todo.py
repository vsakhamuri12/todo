from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from api.db import Todos,User
from api.models import TodosModel, UserModel, TokenData, TodoId
from jose import JWTError, jwt
import time
import os
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

todo_routes = APIRouter()
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def convert_objectid_to_str(obj):
    obj["_id"] = str(obj["_id"])

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

time_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token is Expired",
        headers={"WWW-Authenticate": "Bearer"},
    )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email= payload.get("email")
        timestamp = payload.get("exp")
        if(timestamp < time.time()):
            raise time_exception
        if email is None:
            raise credentials_exception
        Email = TokenData(email=email)
    except JWTError as e:
        print(e)
        raise credentials_exception
    
    user = User.objects(email=Email.email)
    
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(user: UserModel = Depends(get_current_user)):
    for i in user:
        u = i.to_mongo().to_dict()
    u["_id"] = str(u["_id"])
    return u


@todo_routes.post("/create")
async def createpost(todo : TodosModel, user: UserModel = Depends(get_current_active_user)):
    uid = user["_id"]
    todo = todo.dict()
    todo["uid"] = uid
    todoitem = Todos(
        **todo
    )
    re = todoitem.save()
    return {"done" : "done"}

@todo_routes.get("/gettodos")
async def createpost(user: UserModel = Depends(get_current_active_user)):
    todoitems = Todos.objects(
        uid = user["_id"]
    )
    todos = list(map(lambda s: s.to_mongo().to_dict(), todoitems))
    for i in todos:
        convert_objectid_to_str(i)
    return todos

@todo_routes.put("/delete")
async def delpost(todoid : TodoId, user: UserModel = Depends(get_current_active_user)):
    print(todoid.dict())
    todoid = todoid.dict()
    todo = Todos.objects(id=todoid["id"])
    for i in todo:
        todoitem = i.to_mongo().to_dict()
        convert_objectid_to_str(todoitem)
    if(todoitem["uid"] == user["_id"]):
        todo.delete()
    else:
        raise credentials_exception
    
    return {
        "done" : "done"
    }
