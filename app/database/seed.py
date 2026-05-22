from sqlalchemy.orm import Session
from app.models.laboratory import Laboratory

DEFAULT_LABS = ["Spark", "KITE", "CLIC", "ACTION LAB"]


def seed_laboratories(db: Session) -> None:
    for nombre in DEFAULT_LABS:
        if not db.query(Laboratory).filter(Laboratory.nombre == nombre).first():
            db.add(Laboratory(nombre=nombre))
    db.commit()
