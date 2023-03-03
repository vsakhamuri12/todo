import os
from fastapi import FastAPI
from mongoengine import connect, disconnect
from dotenv import load_dotenv
from api.todo import todo_routes
import certifi
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

app = FastAPI()
app.include_router(todo_routes)


@app.on_event("startup")
async def startup():
    connect(host=MONGO_URI, alias="todo", tlsCAFile=certifi.where())


@app.on_event("shutdown")
async def shutdown():
    disconnect(alias="todo")
