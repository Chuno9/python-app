from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path, APIRouter
from starlette import status
from pydantic import BaseModel, Field
from models import Todos, Usuarios
from passlib.context import CryptContext
from database import SessionLocal
from .auth import obtener_usuario

router = APIRouter(
    prefix="/user",
    tags=["user"]
    )

def obtenerDB():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session, Depends(obtenerDB)]
user_dependency=Annotated[dict, Depends(obtener_usuario)]
bcrypt_context=CryptContext(schemes=['bcrypt'], deprecated='auto')

class VerificarUsuario(BaseModel):
    contraseña:str
    nuevaContraseña:str=Path(min_length=6)

class ActualizarTel(BaseModel):
    tel:str

@router.get("/", status_code=status.HTTP_200_OK)
async def datos_usuario(usuario:user_dependency, db:db_dependency):
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No tienes acceso a estos recursos")
    return db.query(Usuarios).filter(Usuarios.id==usuario.get("id")).first()

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def cambiar_contraseña(usuario: user_dependency,db: db_dependency, verificacion:VerificarUsuario):
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No tienes acceso a estos recursos")
    modelo_usuario=db.query(Usuarios).filter(Usuarios.id==usuario.get("id")).first()

    if not bcrypt_context.verify (verificacion.contraseña, modelo_usuario.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No tienes acceso a estos recursos")
    modelo_usuario.hash_password=bcrypt_context.hash(verificacion.nuevaContraseña)
    db.add(modelo_usuario)
    db.commit()

@router.put("/tel", status_code=status.HTTP_204_NO_CONTENT)
async def actualizar_tel(usuario: user_dependency, db: db_dependency, tel: ActualizarTel):
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No tienes acceso a estos recursos")
    modelo_usuario=db.query(Usuarios).filter(Usuarios.id==usuario.get("id")).first()

    modelo_usuario.tel=tel.tel
    db.add(modelo_usuario)
    db.commit()