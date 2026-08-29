from fastapi import FastAPI
from pydantic import BaseModel
import tasks  #importing the tasks.py file in this file

class TaskCreate(BaseModel):
    title:str
    completed:bool = False # the default value is false


app = FastAPI(title="Task Manager API")

@app.get("/")
def read_root():
    return {"message" : "Welcome to your task manager API!"}

@app.get("/tasks")
def get_all_tasks():
    # calling the database helper function from tasks.py
    return tasks.get_tasks_for_web()

@app.get("/tasks/{task_id}")
def get_task_by_id(task_id : int):
    task = tasks.get_task_by_id(task_id)

    if task is None:
        return {"error" : "task with ID {task_id} not found"}
    
    return task

@app.post("/tasks")
def create_task(task : TaskCreate):
    new_task = tasks.add_tasks(task.title,task.completed)
    return new_task
