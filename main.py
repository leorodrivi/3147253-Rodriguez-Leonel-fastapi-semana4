from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal, engine, Base
import models
import schemas
import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Autores y Libros",
    description="Una API para gestionar autores y sus libros",
    version="1.0.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/autores/", response_model=schemas.Autor, status_code=status.HTTP_201_CREATED)
def crear_autor(autor: schemas.AutorCreate, db: Session = Depends(get_db)):
    return crud.crear_autor(db=db, autor=autor)

@app.get("/autores/", response_model=List[schemas.Autor])
def listar_autores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    autores = crud.obtener_autores(db, skip=skip, limit=limit)
    return autores

@app.get("/autores/{autor_id}", response_model=schemas.Autor)
def obtener_autor(autor_id: int, db: Session = Depends(get_db)):
    db_autor = crud.obtener_autor(db, autor_id=autor_id)
    if db_autor is None:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return db_autor

@app.put("/autores/{autor_id}", response_model=schemas.Autor)
def actualizar_autor(autor_id: int, autor: schemas.AutorCreate, db: Session = Depends(get_db)):
    db_autor = crud.actualizar_autor(db, autor_id, autor)
    if db_autor is None:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return db_autor

@app.delete("/autores/{autor_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_autor(autor_id: int, db: Session = Depends(get_db)):
    if not crud.eliminar_autor(db, autor_id):
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return {"message": "Autor eliminado correctamente"}

@app.post("/autores/{autor_id}/libros/", response_model=schemas.Libro, status_code=status.HTTP_201_CREATED)
def crear_libro(autor_id: int, libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    return crud.crear_libro(db=db, libro=libro, autor_id=autor_id)

@app.get("/libros/", response_model=List[schemas.Libro])
def listar_libros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    libros = crud.obtener_libros(db, skip=skip, limit=limit)
    return libros

@app.get("/libros/{libro_id}", response_model=schemas.Libro)
def obtener_libro(libro_id: int, db: Session = Depends(get_db)):
    db_libro = crud.obtener_libro(db, libro_id=libro_id)
    if db_libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return db_libro

@app.put("/libros/{libro_id}", response_model=schemas.Libro)
def actualizar_libro(libro_id: int, libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    db_libro = crud.actualizar_libro(db, libro_id, libro)
    if db_libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return db_libro

@app.delete("/libros/{libro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_libro(libro_id: int, db: Session = Depends(get_db)):
    if not crud.eliminar_libro(db, libro_id):
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return {"message": "Libro eliminado correctamente"}

@app.get("/autores/{autor_id}/libros/", response_model=List[schemas.Libro])
def obtener_libros_autor(autor_id: int, db: Session = Depends(get_db)):
    return crud.obtener_libros_por_autor(db, autor_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)