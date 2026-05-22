from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import get_db, get_current_user, require_roles
from app.schemas.printing_3d import Printing3DCreate, Printing3DUpdate, Printing3DResponse
from app.services.printing_3d_service import Printing3DService

router = APIRouter(prefix="/api/v1/printings-3d", tags=["printings-3d"])


@router.post("/", response_model=Printing3DResponse, status_code=201)
async def create_printing(
    data: Printing3DCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Request a 3D print job.
    - Estudiante: only for themselves (id_usuario forced to their carnet).
    - Admin/Gestor: can create for any user.
    """
    if current_user.role == "estudiante":
        data = Printing3DCreate(
            id_usuario=current_user.carnet,
            id_printer=data.id_printer,
            id_material=data.id_material,
            gramos=data.gramos,
            tiempo_estimado=data.tiempo_estimado,
            tipo_trabajo=data.tipo_trabajo,
        )
    elif current_user.role not in ("admin", "gestor"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not enough permissions")

    printing = Printing3DService(db).create_printing(data)

    # Confirmation email
    from app.repositories.user_repository import UserRepository
    from app.repositories.material_3d_repository import Material3DRepository
    from app.services.email_service import send_printing_3d_email

    user = UserRepository(db).get_by_carnet(data.id_usuario)
    material = Material3DRepository(db).get_by_id(printing.id_material)
    if user and material and printing.printer:
        context = {
            "nombre": user.nombre,
            "carnet": user.carnet,
            "codigo_impresora": printing.printer.codigo,
            "nombre_impresora": printing.printer.nombre or printing.printer.codigo,
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
    id_printer: Optional[int] = None,
    id_usuario: Optional[int] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    - Estudiante: sees only their own print jobs.
    - Admin/Gestor: sees all. Filters: ?id_printer=1 ?estado=pendiente ?id_usuario=X
    """
    if current_user.role == "estudiante":
        id_usuario = current_user.carnet
    elif current_user.role not in ("admin", "gestor"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not enough permissions")

    return Printing3DService(db).get_printings(
        skip=skip, limit=limit,
        id_usuario=id_usuario, id_material=id_material,
        id_printer=id_printer, estado=estado,
    )


@router.get("/{id_impresion}", response_model=Printing3DResponse)
def get_printing(
    id_impresion: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    printing = Printing3DService(db).get_printing(id_impresion)
    if current_user.role == "estudiante" and printing.id_usuario != current_user.carnet:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Cannot view another user's printing job")
    return printing


@router.put("/{id_impresion}", response_model=Printing3DResponse)
def update_printing(
    id_impresion: int,
    data: Printing3DUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "gestor")),
):
    """Admin/Gestor can update details and change estado (pendiente→en_proceso→completado)."""
    return Printing3DService(db).update_printing(id_impresion, data)
