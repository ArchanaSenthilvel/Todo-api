from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict


app = FastAPI()

todolist: Dict[int, Dict[str, str]] = {
    0: {
        "task": "Task 0",
        "description": "description 0",
        "status": "Done"
    }
}


class ToDOList(BaseModel):
    task : str
    description : str
    status : str

class ToDoListPatch(BaseModel):
    task: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

@app.get('/')
async def home():
    return todolist

@app.get('/task_no/{id}')
async def task_no(id: int):
    return todolist.get(id, {"Error": "Task not exist"})

@app.post('/create_task/{id}')
async def create_task(id: int, td: ToDOList):
    if id in todolist:
        return {"Task": "Already Exist"}
    todolist[id] = td.dict()
    return todolist[id]

@app.put("/update_task/{id}")
async def update_task(id: int, td: ToDOList):
    if id not in todolist:
        return {"Error": "Task not Exist"}
    todolist[id] = td.dict()
    return todolist[id]

@app.patch("/patch_task/{id}")
async def patch_task(id: int, td: ToDoListPatch):
    if id not in todolist:
        return {"Error": "Task not Exist"}
    updated_data = td.dict(exclude_unset=True)
    todolist[id].update(updated_data)
    return todolist[id]

@app.delete("/delete_task/{id}")
async def delete_task(id : int):
    if id not in todolist:
        return {"Error" : "task not exist"}
    del todolist[id]
    return {"Message" : "Deleted"}
