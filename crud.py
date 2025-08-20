from sqlalchemy.orm import Session
import models
import schemas

def obtener_autores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Autor).offset(skip).limit(limit).all()

def obtener_autor(db: Session, autor_id: int):
    return db.query(models.Autor).filter(models.Autor.id == autor_id).first()

def crear_autor(db: Session, autor: schemas.AutorCreate):
    db_autor = models.Autor(
        nombre=autor.nombre,
        nacionalidad=autor.nacionalidad,
        fecha_nacimiento=autor.fecha_nacimiento
    )
    db.add(db_autor)
    db.commit()
    db.refresh(db_autor)
    return db_autor

def actualizar_autor(db: Session, autor_id: int, autor: schemas.AutorCreate):
    db_autor = db.query(models.Autor).filter(models.Autor.id == autor_id).first()
    if db_autor:
        for key, value in autor.dict(exclude_unset=True).items():
            setattr(db_autor, key, value)
        db.commit()
        db.refresh(db_autor)
    return db_autor

def eliminar_autor(db: Session, autor_id: int):
    db_autor = db.query(models.Autor).filter(models.Autor.id == autor_id).first()
    if db_autor:
        db.delete(db_autor)
        db.commit()
        return True
    return False

def obtener_libros(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Libro).offset(skip).limit(limit).all()

def obtener_libro(db: Session, libro_id: int):
    return db.query(models.Libro).filter(models.Libro.id == libro_id).first()

def obtener_libros_por_autor(db: Session, autor_id: int):
    return db.query(models.Libro).filter(models.Libro.autor_id == autor_id).all()

def crear_libro(db: Session, libro: schemas.LibroCreate, autor_id: int):
    db_libro = models.Libro(
        **libro.dict(),
        autor_id=autor_id
    )
    db.add(db_libro)
    db.commit()
    db.refresh(db_libro)
    return db_libro

def actualizar_libro(db: Session, libro_id: int, libro: schemas.LibroCreate):
    db_libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if db_libro:
        for key, value in libro.dict(exclude_unset=True).items():
            setattr(db_libro, key, value)
        db.commit()
        db.refresh(db_libro)
    return db_libro

def eliminar_libro(db: Session, libro_id: int):
    db_libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if db_libro:
        db.delete(db_libro)
        db.commit()
        return True
    return False