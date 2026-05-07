from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from database import Base
from main2 import app
from fastapi.testclient import TestClient 
import pytest
from models import Todos, Usuarios
from routers.auth import bcrypt_context
SQLALCHEMY_DATABASE_URL="sqlite:///./testdb.db"

engine=create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},
                     poolclass= StaticPool )

TestingSessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_obtenerDB():
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_obtener_usuario():
    return {"nombre_usu": "yo", "id": 1, "rol": "admin"}

client=TestClient(app)

@pytest.fixture
def test_todo():
    todo=Todos(
        titulo="aprender",
        descripcion="pues hacer cursos tal",
        prioridad=5,
        dueño_id=1,
        completada=False
    )
    db=TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as con:
        con.execute(text("DELETE FROM todos;"))
        con.commit()

@pytest.fixture
def test_usuarios():
    usu=Usuarios(
        nombre_usu="yo",
        email="yo@gmail.com",
        nombre="Manuel",
        apellido="Álvarez",
        hash_password=bcrypt_context.hash("1234"),
        rol="admin",
        tel="684029384"
    )
    db= TestingSessionLocal()
    db.add(usu)
    db.commit()
    yield usu
    with engine.connect() as con:
        con.execute(text("DELETE FROM usuarios;"))
        con.commit()