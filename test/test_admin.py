from .utils import *
from routers.admin import obtenerDB, obtener_usuario
from fastapi import status

app.dependency_overrides[obtenerDB]= override_obtenerDB
app.dependency_overrides[obtener_usuario]=override_obtener_usuario

def test_admin_leer_autenticado(test_todo):
    response =client.get("/admin/todo")
    assert response.status_code==200
    # assert response.json()== [
    #                         {"completada": False, "titulo": "aprender", 
    #                           "descripcion": "pues hacer cursos tal",
    #                           "id":1, "prioridad": 5, "dueño_id":1}
    #                           ]

def test_admin_borrar_todo(test_todo):
    response=client.delete("/admin/todo/1")
    assert response.status_code==204
    db= TestingSessionLocal()
    model= db.query(Todos).filter(Todos.id== 1).first()
    assert model is None

def test_admin_borrar_todo_not_found(test_todo):
    response=client.delete("/admin/todo/99")
    assert response.status_code==404

    

    