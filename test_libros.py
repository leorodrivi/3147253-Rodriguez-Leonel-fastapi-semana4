import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db
from database import Base
from models import Autor, Libro

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_libros.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_crear_autor():
    response = client.post(
        "/autores/",
        json={"nombre": "Test Autor", "nacionalidad": "Testlandia", "fecha_nacimiento": "2000-01-01"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Test Autor"
    assert "id" in data

def test_obtener_autores():
    response = client.get("/autores/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_crear_libro():
    autor_response = client.post(
        "/autores/",
        json={"nombre": "Autor para Libro", "nacionalidad": "Testlandia"}
    )
    autor_id = autor_response.json()["id"]

    response = client.post(
        f"/autores/{autor_id}/libros/",
        json={"titulo": "Test Libro", "isbn": "1234567890", "autor_id": autor_id}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == "Test Libro"
    assert data["autor_id"] == autor_id

if __name__ == "__main__":
    pytest.main([__file__, "-v"])