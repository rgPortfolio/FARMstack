from pydantic.networks import HttpUrl
from model import Todo
from fastapi import FastAPI, HTTPException, responses
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

from database import (
    fetch_all_todos,
    fetch_one_todo, create_todo,
    update_todo, remove_todo
)


origins = ['https://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"ping":"pong"}

@app.get("/api/todo")
async def get_todo():
    return await fetch_all_todos()

@app.get("/api/todo/{title}", response_model=Todo)
async def get_todo_by_id(title):
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"no todo item with this title {title}")

@app.post("/api/todo")
async def post_todo(todo:Todo):
    response = await create_todo(todo.dict())

@app.put("/api/todo/{title}", response_model=Todo)
async def put_todo(title:str, description: str):
    response = await update_todo(title, description)
    if response:
        return response
    raise HTTPException(404, f"no todo item with this title {title}")

@app.delete("/api/todo/{title}")
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return "Successfully deleted todo item"
    raise HTTPException(404, f"no todo item with this title {title}")