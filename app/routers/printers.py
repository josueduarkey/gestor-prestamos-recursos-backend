from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import get_db, get_current_user, require_roles
from app.schemas.printer import PrinterCreate, PrinterUpdate, PrinterResponse
from app.services.printer_service import PrinterService

router = APIRouter(prefix="/api/v1/printers", tags=["printers"])


@router.post("/", response_model=PrinterResponse, status_code=201)
def create_printer(
    data: PrinterCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    """Admin registers a new 3D printer in the system."""
    return PrinterService(db).create_printer(data)


@router.get("/", response_model=List[PrinterResponse])
def list_printers(
    skip: int = 0,
    limit: int = 100,
    id_laboratorio: Optional[int] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    List all printers. Visible to all authenticated users.
    Filters: ?id_laboratorio=1  ?estado=disponible
    """
    return PrinterService(db).get_printers(
        skip=skip, limit=limit, id_laboratorio=id_laboratorio, estado=estado
    )


@router.get("/{id_printer}", response_model=PrinterResponse)
def get_printer(
    id_printer: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return PrinterService(db).get_printer(id_printer)


@router.put("/{id_printer}", response_model=PrinterResponse)
def update_printer(
    id_printer: int,
    data: PrinterUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin", "gestor")),
):
    """Update printer info or change its estado (disponible/en_uso/mantenimiento)."""
    return PrinterService(db).update_printer(id_printer, data)


@router.delete("/{id_printer}", response_model=PrinterResponse)
def delete_printer(
    id_printer: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    return PrinterService(db).delete_printer(id_printer)
