from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from api.db import User
from api.models import UserModel, TokenData
from passlib.context import CryptContext
from jose import JWTError, jwt
import time
import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
user_routes = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def decode_token(token: str):
    user = User.objects(email=token)
    user = UserModel(**user)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
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


@user_routes.get("/user/me")
async def user_me(user: UserModel = Depends(get_current_active_user)):
    return user


@user_routes.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = User.objects(email=form.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )
    for i in user:
        u = i.to_mongo().to_dict()
    u["_id"] = str(u["_id"])

    if not verify_password(form.password,u["password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    email = {"email" : str(u["email"])}
    token = create_access_token(email)
    return {"access_token": token, "token_type": "bearer"}


@user_routes.post("/signup")
async def signup(form: UserModel):
    hash = get_password_hash(form.password)
    user = User(
        first_name=form.first_name,
        last_name=form.last_name,
        email=form.email,
        password=hash,
        disabled=False,
    )
    user.save()
    return {"done": "done"}




def create_access_token(data: dict, expires_delta: int | None = 0):
    to_encode = data.copy()
    if expires_delta:
        expire = time.time() + expires_delta
    else:
        expire = time.time() + (120*60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
