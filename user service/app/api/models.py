from typing import List
from pydantic import BaseModel
from pydantic.networks import EmailStr


# class TodosModel(BaseModel):
#     title: str
#     desc: str
#     tags: List[str]
#     flag: bool
#     date: FutureDate
#     time: datetime.time
#     status: Literal["done", "ndone", "archived"]


class Token(BaseModel):
    access_token: str
    token_type: str

class UserModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    # TODO: Support for password hash
    password: str
    # disabled: bool
class TokenData(BaseModel):
    email: EmailStr | None = None