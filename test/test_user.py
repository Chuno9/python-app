from .utils import *
from routers.user import obtenerDB, obtener_usuario
from fastapi import status

app.dependency_overrides[obtenerDB]= override_obtenerDB
app.dependency_overrides[obtener_usuario]=override_obtener_usuario

def test_usuario_actual(test_usuarios):
    response=client.get("/user")
    response.status_code==200
    assert response.json()["nombre_usu"]=="yo"
    assert response.json()["email"]=="yo@gmail.com"
    assert response.json()["nombre"]=="Manuel"
    assert response.json()["apellido"]=="Álvarez"
    assert response.json()["rol"]=="admin"
    assert response.json()["tel"]=="684029384"

def test_cambiar_contraseña(test_usuarios):
    response=client.put("/user/password", json={"contraseña": "1234", "nuevaContraseña": "123456"})
    assert response.status_code==204

def test_cambiar_contraseña_no_valida(test_usuarios):
    response=client.put("/user/password", json={"contraseña": "no", "nuevaContraseña": "123456"})
    assert response.status_code==401

def test_cambiar_tel(test_usuarios):
    response=client.put("/user/tel", json={"tel":"684326190"})
    assert response.status_code==204