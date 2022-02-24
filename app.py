from datetime import datetime
from typing import Text, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4 as uuid

app = FastAPI()

tasks = []

class Task(BaseModel):
    id: Optional[str]
    title: str
    description: Text
    create_at: datetime = datetime.now()

@app.get('/')
def read_route():
    return {'welcome': 'Welcome to my API'}


@app.get('/tasks')
def get_tasks():
    return tasks

@app.post('/tasks')
def save_tasks(task: Task):
    task.id = str(uuid())
    tasks.append(task.dict())
    return tasks[-1]

@app.get('/tasks/{task_id}')
def get_task(task_id: str):
    for task in tasks:
        if task['id'] == task_id:
            return task
    raise HTTPException(status_code=404, detail='Task not found')

@app.delete('/tasks/{task_id}')
def delete_task(task_id: str):
    for index, task in enumerate(tasks):
        if task['id'] == task_id:
            tasks.pop(index)
            return {'message': 'Task has been deleted succesfully'}
    raise HTTPException(status_code=404, detail='Item not found')


@app.put('/tasks/{task_id}')
def updat_task(task_id: str, updateTask: Task):
    for index, task in enumerate(tasks):
        if task['id'] == task_id:
            tasks[index]['title'] = updateTask.dict()['title']
            tasks[index]['description'] = updateTask.dict()['description']
            return {'message': 'Task has been updated succesfully'}
    raise HTTPException(status_code=404, detail='Item not found')