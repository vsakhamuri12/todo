from typing import List,Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import FutureDate
from datetime import datetime
from pydantic.fields import Field
from api.db import StatusEnum

class TodosModel(BaseModel):
    _id: Optional[str]
    title: str
    desc: Optional[str]
    uid: Optional[str]
    tags: Optional[List[str]]
    flag: Optional[bool] = False
    date: Optional[FutureDate]
    time: Optional[datetime] = datetime.now
    status: StatusEnum = StatusEnum.NDONE


class TodosModelList(BaseModel):
    todos: List[TodosModel]


class UserModel(BaseModel):
    _id: Optional[str]
    first_name: str
    last_name: str
    email: EmailStr
    # TODO: Support for password hash
    password: str

class TokenData(BaseModel):
    email: EmailStr | None = None

class TodoId(BaseModel):
    id: str