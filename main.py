from dataclasses import asdict
from typing import List
from fastapi import FastAPI, HTTPException, status

from models import Task
from schemas import TaskCreate, TaskResponse, TaskUpdate

app = FastAPI(
    title="Task Management API",
    description="A FastAPI app using Pydantic for validation and frozen dataclasses for internal state.",
    version="1.0.0",
)

tasks: dict[int, Task] = {}


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
)
def create_task(task_input: TaskCreate):
    task_data = task_input.model_dump()
    task_id = len(tasks) + 1
    new_task = Task(task_id=task_id, **task_data)
    tasks[task_id] = new_task
    task_dict = asdict(new_task)
    return TaskResponse(**task_dict)


@app.get(
    "/tasks",
    response_model=List[TaskResponse],
    summary="List all tasks",
)
def get_tasks():
    return [TaskResponse(**asdict(task)) for task in tasks.values()]


@app.delete(
    "/tasks/{task_id}",
    summary="Delete a task",
)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    
    del tasks[task_id]
    return {"message": f"Task {task_id} has been deleted successfully"}


@app.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Partially update an existing task",
)
def patch_task(task_id: int, update_data: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    
    update_dict = update_data.model_dump(exclude_unset=True)
    existing_task = tasks[task_id]
    merged_data = asdict(existing_task)
    merged_data.update(update_dict)
    new_task = Task(**merged_data)
    tasks[task_id] = new_task

    return TaskResponse(**asdict(new_task))
