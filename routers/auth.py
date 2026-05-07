from datetime import datetime, timedelta, timezone
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path, APIRouter, Request
from starlette import status
from pydantic import BaseModel, Field
from database import SessionLocal
from models import Usuarios
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi.templating import Jinja2Templates

router=APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SECRET_KEY='21b534a9eab568d77916c8933e701f84509fa8fce038f0b35932546fb3babdb3'
ALGORITHM='HS256'

bcrypt_context=CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer=OAuth2PasswordBearer(tokenUrl="auth/token")

class SolicitudUsuario(BaseModel):
    nombre_usu:str
    email:str
    nombre:str
    apellido:str
    password:str
    rol:str
    tel:str

class Token(BaseModel):
    access_token:str
    token_type:str

def obtenerDB():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session, Depends(obtenerDB)]

templates = Jinja2Templates(directory="templates/")

### páginas ###

@router.get("/login-page")
def login_page(request:Request):
    return templates.TemplateResponse("login.html",{"request": request})

@router.get("/register-page")
def login_page(request:Request):
    return templates.TemplateResponse("register.html",{"request": request})
### Endpoints ###

def autenticacion_usuario(nombre_usu:str, contraseña:str, db):
    usuario=db.query(Usuarios).filter(Usuarios.nombre_usu == nombre_usu).first()
    if not usuario:
        return False
    if not bcrypt_context.verify(contraseña, usuario.hash_password):
        return False
    return usuario

def crear_token(nombre_usu:str, id_usu:int, rol:str, expires_delta:timedelta):

    encode = {"sub": nombre_usu, "id": id_usu, "rol": rol}
    expires=datetime.now(timezone.utc) + expires_delta
    encode.update({"exp":expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def obtener_usuario(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        nombre_usu: str = payload.get("sub")
        id_usu: int = payload.get("id")
        rol_usu:str = payload.get("rol")
        if nombre_usu is None or id_usu is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No tienes acceso a estos recursos")
        return{"nombre_usu": nombre_usu, "id": id_usu, "rol": rol_usu} 
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No tienes acceso a estos recursos")
@router.post("", status_code=status.HTTP_201_CREATED)
async def crear_usuario(db: db_dependency, usuario :SolicitudUsuario):
    usuario=Usuarios(
        email=usuario.email,
        nombre_usu=usuario.nombre_usu,
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        hash_password=bcrypt_context.hash(usuario.password),
        rol=usuario.rol,
        tel=usuario.tel,
        activo=True
    )
    db.add(usuario)
    db.commit()

@router.post("/token", response_model=Token)
async def access_token(form_data : Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    usuario= autenticacion_usuario(form_data.username, form_data.password, db)
    if not usuario:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No tienes acceso a estos recursos")
    access_token= crear_token(usuario.nombre_usu, usuario.id, usuario.rol, timedelta(minutes=20))
    return {"access_token": access_token, "token_type": "bearer"}