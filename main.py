from fastapi import FastAPI, Request,HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))
    )

print(os.getenv("DB_HOST"))
print(os.getenv("DB_USER"))
print(os.getenv("DB_NAME"))
print(os.getenv("DB_PORT"))




app=FastAPI()

app.mount("/static", StaticFiles(directory="static"),name="static")
templates=Jinja2Templates(directory="templates")

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
    mydb=get_db()
    cursor=mydb.cursor(dictionary=True);
    cursor.execute("select * from tasks")
    tasks=cursor.fetchall()
    cursor.close()
    return tasks

@app.post("/tasks")
def add_tasks(task:Task):
    mydb=get_db()
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
    mydb=get_db()
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
    mydb=get_db()
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