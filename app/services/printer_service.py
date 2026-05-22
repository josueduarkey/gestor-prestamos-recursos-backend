from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.repositories.printer_repository import PrinterRepository
from app.models.printer import Printer
from app.schemas.printer import PrinterCreate, PrinterUpdate, VALID_ESTADOS


class PrinterService:
    def __init__(self, db: Session):
        self.repo = PrinterRepository(db)

    def create_printer(self, data: PrinterCreate) -> Printer:
        if data.estado not in VALID_ESTADOS:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Invalid estado. Valid: {VALID_ESTADOS}")
        if self.repo.get_by_codigo(data.codigo):
            raise HTTPException(status.HTTP_409_CONFLICT, f"Printer '{data.codigo}' already exists")
        printer = Printer(
            codigo=data.codigo,
            nombre=data.nombre,
            estado=data.estado,
            id_laboratorio=data.id_laboratorio,
        )
        return self.repo.create(printer)

    def get_printer(self, id_printer: int) -> Printer:
        printer = self.repo.get_by_id(id_printer)
        if not printer:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Printer not found")
        return printer

    def get_printers(
        self,
        skip: int = 0,
        limit: int = 100,
        id_laboratorio: Optional[int] = None,
        estado: Optional[str] = None,
    ):
        return self.repo.get_all(skip=skip, limit=limit, id_laboratorio=id_laboratorio, estado=estado)

    def update_printer(self, id_printer: int, data: PrinterUpdate) -> Printer:
        printer = self.get_printer(id_printer)
        if data.estado and data.estado not in VALID_ESTADOS:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Invalid estado. Valid: {VALID_ESTADOS}")
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(printer, field, value)
        return self.repo.save(printer)

    def delete_printer(self, id_printer: int) -> Printer:
        printer = self.get_printer(id_printer)
        return self.repo.delete(printer)
