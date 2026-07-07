from fastapi import FastAPI, Request,HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
app=FastAPI()

app.mount("/static", StaticFiles(directory="static"),name="static")
templates=Jinja2Templates(directory="templates")
origins=[
    "http://127.0.0.1:51840",
    "http://127.0.0.1:49425"
]

class Task(BaseModel):
    title:str

tasks = [

{"id": 1, "title": "Study FastAPI", "completed": False},

{"id": 2, "title": "Build a project", "completed": True},

{"id": 3, "title": "Learn Football", "completed": False}
]

@app.get("/")
def home(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def add_tasks(task:Task):
    new_task={
        "id":max(task["id"] for task in tasks)+1 if len(tasks)!=0 else 1,
        "title":task.title,
        "completed":False
    }
    tasks.append(new_task)
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id:int):
    for idx,task in enumerate(tasks):
        if(task["id"]==task_id):
            deleted_task=tasks.pop(idx)
            return deleted_task
    raise HTTPException(
        status_code=404,
        detail="Task not Found"
    )

class UpdatedTask(BaseModel):
    completed:bool

@app.put("/tasks/{task_id}")
def update_task(task_id:int, updated_task:UpdatedTask):
    for task in tasks:
        if task["id"]==task_id:
            task["completed"]= updated_task.completed
            return task
    raise HTTPException(
        status_code=404,
        detail="Task not Found"
    )