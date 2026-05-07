from .utils import *
from routers.auth import obtenerDB, obtener_usuario, autenticacion_usuario, crear_token, SECRET_KEY, ALGORITHM
from fastapi import status, HTTPException
from jose import jwt
from datetime import timedelta
import pytest

app.dependency_overrides[obtenerDB]= override_obtenerDB

def test_autenticacion(test_usuarios):
    db= TestingSessionLocal()
    usuario_autenticado=autenticacion_usuario(test_usuarios.nombre_usu, "1234", db)
    assert usuario_autenticado is not None
    assert usuario_autenticado.nombre_usu==test_usuarios.nombre_usu

def test_crear_token():
    nombre_usu="yo"
    id_usu=1
    rol="admin"
    expires_delta=timedelta(days=1)

    token=crear_token(nombre_usu, id_usu, rol, expires_delta)

    decoded_token=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature":False})
    
    assert decoded_token["sub"]==nombre_usu
    assert decoded_token["id"]==id_usu
    assert decoded_token["rol"]==rol

@pytest.mark.asyncio
async def test_obtener_usuario():
    encode= {"sub": "yo", "id": 1, "rol": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    usuario= await obtener_usuario(token=token)
    assert usuario== {"nombre_usu": "yo", "id": 1, "rol": "admin"}

@pytest.mark.asyncio
async def test_obtener_usuario_payload():
    encode= {"rol": "user"}
    token= jwt.encode(encode, SECRET_KEY, algorithm= ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await obtener_usuario(token=token)
    
    assert excinfo.value.status_code==401
    