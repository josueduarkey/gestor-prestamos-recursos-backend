from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.printing_3d_repository import Printing3DRepository
from app.repositories.material_3d_repository import Material3DRepository
from app.repositories.printer_repository import PrinterRepository
from app.repositories.user_repository import UserRepository
from app.models.printing_3d import Printing3D
from app.schemas.printing_3d import Printing3DCreate, Printing3DUpdate, VALID_ESTADOS
from typing import Optional


class Printing3DService:
    def __init__(self, db: Session):
        self.repo = Printing3DRepository(db)
        self.material_repo = Material3DRepository(db)
        self.printer_repo = PrinterRepository(db)
        self.user_repo = UserRepository(db)

    def create_printing(self, data: Printing3DCreate) -> Printing3D:
        if not self.user_repo.get_by_carnet(data.id_usuario):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        if not self.material_repo.get_by_id(data.id_material):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Material not found")

        printer = self.printer_repo.get_by_id(data.id_printer)
        if not printer:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Printer not found")
        if printer.estado != "disponible":
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Printer '{printer.codigo}' is not available (estado: {printer.estado})",
            )

        printing = Printing3D(
            id_usuario=data.id_usuario,
            id_printer=data.id_printer,
            id_material=data.id_material,
            gramos=data.gramos,
            tiempo_estimado=data.tiempo_estimado,
            tipo_trabajo=data.tipo_trabajo,
            estado="pendiente",
            fecha_solicitud=datetime.now(timezone.utc),
        )
        return self.repo.create(printing)

    def get_printing(self, id_impresion: int) -> Printing3D:
        printing = self.repo.get_by_id(id_impresion)
        if not printing:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Printing job not found")
        return printing

    def get_printings(
        self,
        skip: int = 0,
        limit: int = 100,
        id_usuario: Optional[int] = None,
        id_material: Optional[int] = None,
        id_printer: Optional[int] = None,
        estado: Optional[str] = None,
    ):
        return self.repo.get_all(
            skip=skip, limit=limit,
            id_usuario=id_usuario, id_material=id_material,
            id_printer=id_printer, estado=estado,
        )

    def update_printing(self, id_impresion: int, data: Printing3DUpdate) -> Printing3D:
        printing = self.get_printing(id_impresion)
        if data.estado and data.estado not in VALID_ESTADOS:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Invalid estado. Valid: {VALID_ESTADOS}",
            )
        if data.id_printer and not self.printer_repo.get_by_id(data.id_printer):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Printer not found")
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(printing, field, value)
        return self.repo.save(printing)
