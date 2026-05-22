from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.printing_3d_repository import Printing3DRepository
from app.repositories.loan_repository import LoanRepository
from app.repositories.material_3d_repository import Material3DRepository
from app.models.printing_3d import Printing3D
from app.schemas.printing_3d import Printing3DCreate, Printing3DUpdate
from typing import Optional


class Printing3DService:
    def __init__(self, db: Session):
        self.repo = Printing3DRepository(db)
        self.loan_repo = LoanRepository(db)
        self.material_repo = Material3DRepository(db)

    def create_printing(self, data: Printing3DCreate) -> Printing3D:
        if not self.loan_repo.get_by_id(data.id_loan):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Loan not found")
        if not self.material_repo.get_by_id(data.id_material):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Material not found")
        if self.repo.get_by_loan(data.id_loan):
            raise HTTPException(status.HTTP_409_CONFLICT, "Printing job already registered for this loan")

        printing = Printing3D(**data.model_dump())
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
        id_material: Optional[int] = None,
        codigo_impresora: Optional[str] = None,
    ):
        return self.repo.get_all(
            skip=skip, limit=limit, id_material=id_material, codigo_impresora=codigo_impresora
        )

    def update_printing(self, id_impresion: int, data: Printing3DUpdate) -> Printing3D:
        printing = self.get_printing(id_impresion)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(printing, field, value)
        return self.repo.save(printing)
