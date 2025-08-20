from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class AutorBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, example="Gabriel García Márquez")
    nacionalidad: Optional[str] = Field(None, max_length=50, example="Colombiano")
    fecha_nacimiento: Optional[str] = Field(None, example="1927-03-06")

class AutorCreate(AutorBase):
    pass

class Autor(AutorBase):
    id: int
    
    class Config:
        orm_mode = True

class LibroBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200, example="Cien años de soledad")
    isbn: str = Field(..., min_length=10, max_length=20, example="978-8437604947")
    fecha_publicacion: Optional[str] = Field(None, example="1967-05-30")
    genero: Optional[str] = Field(None, max_length=50, example="Realismo mágico")

class LibroCreate(LibroBase):
    autor_id: int

class Libro(LibroBase):
    id: int
    autor_id: int
    
    class Config:
        orm_mode = True

class LibroConAutor(Libro):
    autor: Autor