from fastapi import FastAPI, HTTPException, status
from models import Task, TaskCreate
from data_handler import TaskDataHandler
from typing import List, Optional

import logging

app = FastAPI()
handler = TaskDataHandler()

logging.basicConfig(level=logging.INFO)

@app.get("/")
def read_root():
    return {"message": "Task Management API is running."}

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    try:
        new_task = handler.create_task(task)
        logging.info("Task created: %s", new_task)
        return new_task
    except Exception as e:
        logging.error("Error: %s", e)
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/tasks", response_model=List[Task])
async def list_tasks(is_completed: Optional[bool]=None):
    return handler.get_tasks(is_completed=is_completed)

@app.put("/tasks/{task_id}", response_model=Task)
async def mark_task_completed(task_id: str):
    task = handler.mark_completed(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    logging.info("Task marked completed: %s", task)
    return task

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: str):
    deleted = handler.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    logging.info("Task deleted: %s", task_id)
