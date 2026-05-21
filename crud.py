from sqlalchemy.orm import Session
from typing import Optional
import models, schemas


# -------------------- USERS --------------------
def get_user(db: Session, carnet: int):
    return db.query(models.User).filter(models.User.carnet == carnet).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed = user.password + "notreallyhashed"  # Usa passlib en producción
    db_user = models.User(**user.dict(exclude={"password"}), password=fake_hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, carnet: int, user_update: schemas.UserCreate):
    db_user = get_user(db, carnet)
    if db_user:
        for key, value in user_update.dict().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, carnet: int):
    db_user = get_user(db, carnet)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


# -------------------- LABORATORIES --------------------
def get_laboratory(db: Session, id_laboratorio: int):
    return db.query(models.Laboratory).filter(models.Laboratory.id_laboratorio == id_laboratorio).first()

def get_laboratories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Laboratory).offset(skip).limit(limit).all()

def create_laboratory(db: Session, laboratory: schemas.LaboratoryCreate):
    db_lab = models.Laboratory(**laboratory.dict())
    db.add(db_lab)
    db.commit()
    db.refresh(db_lab)
    return db_lab

def update_laboratory(db: Session, id_laboratorio: int, laboratory_update: schemas.LaboratoryCreate):
    db_lab = get_laboratory(db, id_laboratorio)
    if db_lab:
        for key, value in laboratory_update.dict().items():
            setattr(db_lab, key, value)
        db.commit()
        db.refresh(db_lab)
    return db_lab

def delete_laboratory(db: Session, id_laboratorio: int):
    db_lab = get_laboratory(db, id_laboratorio)
    if db_lab:
        db.delete(db_lab)
        db.commit()
    return db_lab


# -------------------- RESOURCES --------------------
def get_resource(db: Session, id_recurso: int):
    return db.query(models.Resource).filter(models.Resource.id_recurso == id_recurso).first()

def get_resource_by_codigo(db: Session, codigo: str):
    return db.query(models.Resource).filter(models.Resource.codigo == codigo).first()

def get_resources(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    categoria: Optional[str] = None,
    id_laboratorio: Optional[int] = None,
):
    query = db.query(models.Resource)
    if categoria:
        query = query.filter(models.Resource.categoria == categoria)
    if id_laboratorio:
        query = query.filter(models.Resource.id_laboratorio == id_laboratorio)
    return query.offset(skip).limit(limit).all()

def create_resource(db: Session, resource: schemas.ResourceCreate):
    db_resource = models.Resource(**resource.dict())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def update_resource(db: Session, id_recurso: int, resource_update: schemas.ResourceCreate):
    db_resource = get_resource(db, id_recurso)
    if db_resource:
        for key, value in resource_update.dict().items():
            setattr(db_resource, key, value)
        db.commit()
        db.refresh(db_resource)
    return db_resource

def delete_resource(db: Session, id_recurso: int):
    db_resource = get_resource(db, id_recurso)
    if db_resource:
        db.delete(db_resource)
        db.commit()
    return db_resource


# -------------------- PRESTAMOS --------------------
def get_prestamo(db: Session, id_prestamo: int):
    return db.query(models.Prestamo).filter(models.Prestamo.id_prestamo == id_prestamo).first()

def get_prestamos(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    id_usuario: Optional[int] = None,
    estado: Optional[bool] = None,
):
    query = db.query(models.Prestamo)
    if id_usuario is not None:
        query = query.filter(models.Prestamo.id_usuario == id_usuario)
    if estado is not None:
        query = query.filter(models.Prestamo.estado == estado)
    return query.offset(skip).limit(limit).all()

def create_prestamo(db: Session, prestamo: schemas.PrestamoCreate):
    db_prestamo = models.Prestamo(**prestamo.dict())
    db.add(db_prestamo)
    db.commit()
    db.refresh(db_prestamo)
    return db_prestamo

def update_prestamo(db: Session, id_prestamo: int, prestamo_update: schemas.PrestamoCreate):
    db_prestamo = get_prestamo(db, id_prestamo)
    if db_prestamo:
        for key, value in prestamo_update.dict().items():
            setattr(db_prestamo, key, value)
        db.commit()
        db.refresh(db_prestamo)
    return db_prestamo

def delete_prestamo(db: Session, id_prestamo: int):
    db_prestamo = get_prestamo(db, id_prestamo)
    if db_prestamo:
        db.delete(db_prestamo)
        db.commit()
    return db_prestamo


# -------------------- LOAN DETAILS --------------------
def get_loan_detail(db: Session, id_detalle: int):
    return db.query(models.LoanDetail).filter(models.LoanDetail.id_detalle == id_detalle).first()

def get_loan_details(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    id_prestamo: Optional[int] = None,
):
    query = db.query(models.LoanDetail)
    if id_prestamo is not None:
        query = query.filter(models.LoanDetail.id_prestamo == id_prestamo)
    return query.offset(skip).limit(limit).all()

def create_loan_detail(db: Session, loan_detail: schemas.LoanDetailCreate):
    db_detail = models.LoanDetail(**loan_detail.dict())
    db.add(db_detail)
    db.commit()
    db.refresh(db_detail)
    return db_detail

def update_loan_detail(db: Session, id_detalle: int, loan_detail_update: schemas.LoanDetailCreate):
    db_detail = get_loan_detail(db, id_detalle)
    if db_detail:
        for key, value in loan_detail_update.dict().items():
            setattr(db_detail, key, value)
        db.commit()
        db.refresh(db_detail)
    return db_detail

def delete_loan_detail(db: Session, id_detalle: int):
    db_detail = get_loan_detail(db, id_detalle)
    if db_detail:
        db.delete(db_detail)
        db.commit()
    return db_detail


# -------------------- RETURNS --------------------
def get_return(db: Session, id_devolucion: int):
    return db.query(models.Return).filter(models.Return.id_devolucion == id_devolucion).first()

def get_returns(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    id_prestamo: Optional[int] = None,
    estado: Optional[bool] = None,
):
    query = db.query(models.Return)
    if id_prestamo is not None:
        query = query.filter(models.Return.id_prestamo == id_prestamo)
    if estado is not None:
        query = query.filter(models.Return.estado == estado)
    return query.offset(skip).limit(limit).all()

def create_return(db: Session, return_data: schemas.ReturnCreate):
    db_return = models.Return(**return_data.dict())
    db.add(db_return)
    db.commit()
    db.refresh(db_return)
    return db_return

def update_return(db: Session, id_devolucion: int, return_update: schemas.ReturnCreate):
    db_return = get_return(db, id_devolucion)
    if db_return:
        for key, value in return_update.dict().items():
            setattr(db_return, key, value)
        db.commit()
        db.refresh(db_return)
    return db_return

def delete_return(db: Session, id_devolucion: int):
    db_return = get_return(db, id_devolucion)
    if db_return:
        db.delete(db_return)
        db.commit()
    return db_return


# -------------------- MATERIAL 3D --------------------
def get_material_3d(db: Session, id_material: int):
    return db.query(models.Material3D).filter(models.Material3D.id_material == id_material).first()

def get_materials_3d(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Material3D).offset(skip).limit(limit).all()

def create_material_3d(db: Session, material: schemas.Material3DCreate):
    db_material = models.Material3D(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

def update_material_3d(db: Session, id_material: int, material_update: schemas.Material3DCreate):
    db_material = get_material_3d(db, id_material)
    if db_material:
        for key, value in material_update.dict().items():
            setattr(db_material, key, value)
        db.commit()
        db.refresh(db_material)
    return db_material

def delete_material_3d(db: Session, id_material: int):
    db_material = get_material_3d(db, id_material)
    if db_material:
        db.delete(db_material)
        db.commit()
    return db_material


# -------------------- PRINTING 3D --------------------
def get_printing_3d(db: Session, id_impresion: int):
    return db.query(models.Printing3D).filter(models.Printing3D.id_impresion == id_impresion).first()

def get_printings_3d(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    id_prestamo: Optional[int] = None,
    id_material: Optional[int] = None,
):
    query = db.query(models.Printing3D)
    if id_prestamo is not None:
        query = query.filter(models.Printing3D.id_prestamo == id_prestamo)
    if id_material is not None:
        query = query.filter(models.Printing3D.id_material == id_material)
    return query.offset(skip).limit(limit).all()

def create_printing_3d(db: Session, printing: schemas.Printing3DCreate):
    db_printing = models.Printing3D(**printing.dict())
    db.add(db_printing)
    db.commit()
    db.refresh(db_printing)
    return db_printing

def update_printing_3d(db: Session, id_impresion: int, printing_update: schemas.Printing3DCreate):
    db_printing = get_printing_3d(db, id_impresion)
    if db_printing:
        for key, value in printing_update.dict().items():
            setattr(db_printing, key, value)
        db.commit()
        db.refresh(db_printing)
    return db_printing

def delete_printing_3d(db: Session, id_impresion: int):
    db_printing = get_printing_3d(db, id_impresion)
    if db_printing:
        db.delete(db_printing)
        db.commit()
    return db_printing