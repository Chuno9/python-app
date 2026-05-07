import pytest

def test_equal():
    assert 3==3
    assert 3!=1

def test_instance():
    assert isinstance("string",str)
    assert not isinstance("10", int)

def test_boolean():
    validacion=True
    assert validacion==True
    assert ("hola"=="mundo") is False

def test_type():
    assert type("hola" is str)
    assert type ('mundo' is not int)

def test_mayor_menor():
    assert 7>3
    assert 4<10

def test_list():
    num_list=[1,2,3,4,5]
    lista=[False, False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(lista)

class Estudiante():
    def __init__(self, nombre: str, apellido: str, modulo: str, edad: int):
        self.nombre=nombre
        self.apellido=apellido
        self.modulo=modulo
        self.edad=edad

@pytest.fixture
def default_persona():
    return Estudiante("yo", "real", "DAW", 20)

def test_persona(default_persona):
    assert default_persona.nombre=="yo", "El nombre debería ser yo"
    assert default_persona.apellido=="real", "el apellido debería ser real"
    assert default_persona.modulo=="DAW", "Tiene que serlo"
    assert default_persona.edad==20