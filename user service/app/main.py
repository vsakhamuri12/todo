import os
from fastapi import FastAPI
from mongoengine import connect, disconnect
from dotenv import load_dotenv
from api.user import user_routes
import certifi
import uvicorn
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

app = FastAPI()
app.include_router(user_routes)


@app.on_event("startup")
async def startup():
    connect(host=MONGO_URI, alias="todo", tlsCAFile=certifi.where())


@app.on_event("shutdown")
async def shutdown():
    disconnect(alias="todo")
