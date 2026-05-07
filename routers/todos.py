from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path, APIRouter, Request
from starlette import status
from pydantic import BaseModel, Field
from database import SessionLocal
from models import Todos
from .auth import obtener_usuario
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

templates=Jinja2Templates(directory="templates/")

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

def obtenerDB():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session, Depends(obtenerDB)]
user_dependency=Annotated[dict, Depends(obtener_usuario)]

class SolicitudTodo(BaseModel):
    titulo:str=Field(min_length=3)
    descripcion:str=Field(min_length=3, max_length=100)
    prioridad:int=Field(gt=0, lt=6)
    completada:bool

def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


### paginas ###

@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await obtener_usuario(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()

        todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

        return templates.TemplateResponse("todo.html", {"request": request, "todos": todos, "user": user})

    except:
        return redirect_to_login()

@router.get('/add-todo-page')
async def render_todo_page(request: Request):
    try:
        user = await obtener_usuario(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})

    except:
        return redirect_to_login()


@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, todo_id: int, db: db_dependency):
    try:
        user = await obtener_usuario(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()

        todo = db.query(Todos).filter(Todos.id == todo_id).first()

        return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user})

    except:
        return redirect_to_login()
### Endpoints ###

@router.get("/", status_code=status.HTTP_200_OK)
async def leerDatos(usuario: user_dependency, db: db_dependency):
    if usuario is None:
        raise HTTPException(status_code=401, detail="Autenticacion fallida")
    return db.query(Todos).filter(Todos.dueño_id==usuario.get("id")).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def datosPorId(usuario:user_dependency, db: db_dependency, todo_id: int=Path(gt=0)):
    if usuario is None:
        raise HTTPException(status_code=401, detail="Autenticacion fallida")
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.dueño_id==usuario.get("id")).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="No encontrado")

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def crear_Todo(usuario:user_dependency, db:db_dependency, solicitud:SolicitudTodo):
    if usuario is None:
        raise HTTPException(status_code=401, detail="Autenticacion fallida")
    todo_model=Todos(**solicitud.dict(), dueño_id=usuario.get("id"))

    db.add(todo_model)
    db.commit()

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def actualizarTodo(usuario: user_dependency, db: db_dependency, solicitud:SolicitudTodo, todo_id:int=Path(gt=0)):
    if usuario is None:
        raise HTTPException(status_code=401, detail="Autenticacion fallida")
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.dueño_id==usuario.get("id")).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="no se encuentra la tarea")
    todo_model.titulo=solicitud.titulo
    todo_model.descripcion=solicitud.descripcion
    todo_model.prioridad=solicitud.prioridad
    todo_model.completada=solicitud.completada
    db.add(todo_model)
    db.commit()
    
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def borrarTodo(usuario: user_dependency, db: db_dependency, todo_id:int = Path(gt=0)):
    if usuario is None:
        raise HTTPException(status_code=401, detail="Autenticacion fallida")
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.dueño_id==usuario.get("id")).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="no se encuentra la tarea")
    db.query(Todos).filter(Todos.id==todo_id).delete()
    db.commit()