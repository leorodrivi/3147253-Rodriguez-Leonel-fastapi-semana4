from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Autor(Base):
    __tablename__ = "autores"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    nacionalidad = Column(String)
    fecha_nacimiento = Column(String)

    libros = relationship("Libro", back_populates="autor")

class Libro(Base):
    __tablename__ = "libros"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True, nullable=False)
    isbn = Column(String, unique=True, index=True)
    fecha_publicacion = Column(String)
    genero = Column(String)

    autor_id = Column(Integer, ForeignKey("autores.id"))

    autor = relationship("Autor", back_populates="libros")