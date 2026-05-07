from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path, APIRouter
from starlette import status
from pydantic import BaseModel, Field
from models import Todos
from database import SessionLocal
from .auth import obtener_usuario

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
    )

def obtenerDB():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session, Depends(obtenerDB)]
user_dependency=Annotated[dict, Depends(obtener_usuario)]

@router.get("/todo", status_code=status.HTTP_200_OK)
async def obtener_todo(usuario: user_dependency, db: db_dependency):
    if usuario is None or usuario.get("rol")!= "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No tienes acceso a estos recursos")
    return db.query(Todos).all

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def borrar_Todo(usuario: user_dependency, db: db_dependency, todo_id:int = Path(gt=0)):
    if usuario is None or usuario.get("rol")!= "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No tienes acceso a estos recursos")
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="no se encuentra la tarea")
    db.query(Todos).filter(Todos.id==todo_id).delete()
    db.commit()