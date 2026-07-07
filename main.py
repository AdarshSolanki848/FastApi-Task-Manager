from fastapi import FastAPI, Request,HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import mysql.connector
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",
    database="TaskManager"
)





app=FastAPI()

app.mount("/static", StaticFiles(directory="static"),name="static")
templates=Jinja2Templates(directory="templates")
origins=[
    "http://127.0.0.1:51840",
    "http://127.0.0.1:49425"
]

class Task(BaseModel):
    title:str


@app.get("/")
def home(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.get("/tasks")
def get_tasks():
    cursor=mydb.cursor(dictionary=True);
    cursor.execute("select * from tasks")
    tasks=cursor.fetchall()
    cursor.close()
    return tasks

@app.post("/tasks")
def add_tasks(task:Task):
    cursor=mydb.cursor()
    query="Insert into tasks(title,completed) values(%s,%s)"
    values=(task.title,False)
    cursor.execute(query,values)
    mydb.commit()
    new_task={
        "id":cursor.lastrowid,
        "title":task.title,
        "completed":False
    }
    cursor.close()
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id:int):
    cursor=mydb.cursor(dictionary=True)

    query="Delete from tasks where id=%s";
    cursor.execute(query,(task_id,))

    if(cursor.rowcount==0):
        cursor.close()
        raise HTTPException(
            status_code=404,
            detail="Task not Found"
        )
    mydb.commit()
    cursor.close()
    return {
        "message":"Task Deleted Successfully"
    }

class UpdatedTask(BaseModel):
    completed:bool

@app.put("/tasks/{task_id}")
def update_task(task_id:int, updated_task:UpdatedTask):
    cursor=mydb.cursor()
    query="update tasks set completed=%s where id=%s"
    values=(updated_task.completed,task_id)
    cursor.execute(query,values)
    if(cursor.rowcount==0):
        cursor.close()
        raise HTTPException(
            status_code=404,
            detail="Task not Found"
        )
    mydb.commit()
    cursor.close()
    return{
        "message":"Task updated Successfully"
    }