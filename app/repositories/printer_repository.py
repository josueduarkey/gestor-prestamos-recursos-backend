from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.printer import Printer


class PrinterRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_printer: int) -> Optional[Printer]:
        return self.db.query(Printer).filter(Printer.id_printer == id_printer).first()

    def get_by_codigo(self, codigo: str) -> Optional[Printer]:
        return self.db.query(Printer).filter(Printer.codigo == codigo).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        id_laboratorio: Optional[int] = None,
        estado: Optional[str] = None,
    ) -> List[Printer]:
        query = self.db.query(Printer)
        if id_laboratorio is not None:
            query = query.filter(Printer.id_laboratorio == id_laboratorio)
        if estado:
            query = query.filter(Printer.estado == estado)
        return query.offset(skip).limit(limit).all()

    def create(self, printer: Printer) -> Printer:
        self.db.add(printer)
        self.db.commit()
        self.db.refresh(printer)
        return printer

    def save(self, printer: Printer) -> Printer:
        self.db.commit()
        self.db.refresh(printer)
        return printer

    def delete(self, printer: Printer) -> Printer:
        self.db.delete(printer)
        self.db.commit()
        return printer
