from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Usuarios(Base):
    __tablename__="usuarios"

    id=Column(Integer, primary_key=True, index=True)
    email=Column(String, unique=True)
    nombre_usu=Column(String)
    nombre=Column(String)
    apellido=Column(String)
    hash_password=Column(String)
    activo=Column(Boolean, default=True)
    rol=Column(String)    
    tel=Column(String)

class Todos(Base):
    __tablename__="todos"

    id=Column(Integer, primary_key=True, index=True)
    titulo=Column(String)
    descripcion=Column(String)
    prioridad=Column(Integer)
    completada=Column(Boolean, default=False)
    dueño_id=Column(Integer, ForeignKey(Usuarios.id))
