from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import get_db, require_roles
from app.schemas.printing_3d import Printing3DCreate, Printing3DUpdate, Printing3DResponse
from app.services.printing_3d_service import Printing3DService

router = APIRouter(prefix="/api/v1/printings-3d", tags=["printings-3d"])


@router.post("/", response_model=Printing3DResponse, status_code=201)
async def create_printing(
    data: Printing3DCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "gestor")),
):
    printing = Printing3DService(db).create_printing(data)

    # Send confirmation email to the student
    from app.repositories.loan_repository import LoanRepository
    from app.repositories.user_repository import UserRepository
    from app.repositories.material_3d_repository import Material3DRepository
    from app.services.email_service import send_printing_3d_email

    loan = LoanRepository(db).get_by_id(printing.id_loan)
    if loan:
        user = UserRepository(db).get_by_carnet(loan.id_usuario)
        material = Material3DRepository(db).get_by_id(printing.id_material)
        if user and material:
            context = {
                "nombre": user.nombre,
                "carnet": user.carnet,
                "codigo_devolucion": loan.codigo_devolucion,
                "codigo_impresora": printing.codigo_impresora,
                "tipo_material": material.tipo_material,
                "gramos": printing.gramos,
                "tiempo_estimado": printing.tiempo_estimado,
                "tipo_trabajo": printing.tipo_trabajo or "Individual",
            }
            background_tasks.add_task(send_printing_3d_email, user.correo, context)

    return printing


@router.get("/", response_model=List[Printing3DResponse])
def list_printings(
    skip: int = 0,
    limit: int = 100,
    id_material: Optional[int] = None,
    codigo_impresora: Optional[str] = None,
    id_usuario: Optional[int] = None,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "gestor")),
):
    return Printing3DService(db).get_printings(
        skip=skip, limit=limit,
        id_material=id_material, codigo_impresora=codigo_impresora, id_usuario=id_usuario,
    )


@router.get("/{id_impresion}", response_model=Printing3DResponse)
def get_printing(
    id_impresion: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "gestor")),
):
    return Printing3DService(db).get_printing(id_impresion)


@router.put("/{id_impresion}", response_model=Printing3DResponse)
def update_printing(
    id_impresion: int,
    data: Printing3DUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "gestor")),
):
    return Printing3DService(db).update_printing(id_impresion, data)
