from fastapi import Depends, FastAPI
from pydantic import BaseModel
import tasks  #importing the tasks.py file in this file
from database import get_db,create_tables

app = FastAPI(title="Task Manager API")

class TaskCreate(BaseModel):
    title:str
    completed:bool = False # the default value is false

@app.on_event("startup")
def on_startup():
    create_tables()
@app.get("/")
def read_root():
    return {"message" : "Welcome to your task manager API!"}

@app.get("/tasks")
def get_all_tasks(conn=Depends(get_db())):
    # calling the database helper function from tasks.py
    return tasks.get_tasks_for_web(conn)

@app.get("/tasks/{task_id}")
def get_task_by_id(task_id : int):
    task = tasks.get_task_by_id(task_id)

    if task is None:
        return {"error" : f"task with ID {task_id} not found"}
    
    return task

@app.post("/tasks")
def create_task(task : TaskCreate):
    new_task = tasks.add_tasks(task.title,task.completed)
    return new_task

@app.patch("/tasks/{task_id}")
def toggle_task_status(task_id : int):
    updated_task = tasks.toggle_task(task_id)

    if updated_task is None:
        return {"error" : f"task with ID {task_id} does not exist"}

    return updated_task

@app.delete("/tasks/{task_id}")
def delete_task_req(task_id : int):
    updated_tasks = tasks.delete_task(task_id)
    if updated_tasks is None:
        return {"error" : f"task with ID {task_id} does not exist"}

    return updated_tasks


