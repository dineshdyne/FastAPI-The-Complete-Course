from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine, SessionLocal # check the database.py
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
#from auth import get_current_user, get_user_exception

app = FastAPI()


models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

class Todo(BaseModel):
    title : str
    description : Optional[str]
    priority : int =Field(gt=0,lt=6,description='Priority must be between 1 and 5')
    complete : bool 

@app.get("/")
async def read_all(db:Session=Depends(get_db)):
    return db.query(models.Todos).all()

# @app.get("/")
# async def create_database():
#     return {"Database":'Created'}

@app.get("/todo/{todo_id}")
async def get_todo_by_id(todo_id:int,db:Session=Depends(get_db)):
    todo_model=db.query(models.Todos).filter(models.Todos.id==todo_id).first()
    if todo_model is not None:
        return todo_model 
    raise http_exception()



    
@app.post("/")
async def create_todo(todo:Todo,db:Session=Depends(get_db)):
    todo_model=models.Todos()
    todo_model.title=todo.title
    todo_model.description = todo.description
    todo_model.priority=todo.priority
    todo_model.complete=todo.complete

    db.add(todo_model)
    db.commit()
    return successful_response(201)

    
@app.put("/{todo_id}")
async def update_todo(todo_id:int,todo:Todo,db:Session=Depends(get_db)):
    todo_model=db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is None:
        raise http_exception()


    
    todo_model.title=todo.title
    todo_model.description = todo.description
    todo_model.priority=todo.priority
    todo_model.complete=todo.complete

    db.add(todo_model)
    db.commit()
    

    return successful_response(200)


@app.delete("/{todo_id}")
async def delete_todo(todo_id:int,db:Session=Depends(get_db)):
    todo_model=db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is None:
        raise http_exception()

    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()
    

    return successful_response(200)


def successful_response(status_code:int):
    return {'status_code': status_code,'transaction':'successful'}




def http_exception():
    return HTTPException(status_code=404,detail="Could not find item")