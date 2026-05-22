from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime


class ResourceByLab(BaseModel):
    laboratorio: str
    total_recursos: int


class RecentLoanItem(BaseModel):
    id_loan: int
    id_usuario: int
    codigo_devolucion: str
    estado: str
    fecha_prestamo: Optional[datetime] = None
    fecha_limite: Optional[datetime] = None


class PenaltyUserItem(BaseModel):
    carnet: int
    nombre: str
    penalizaciones: int


class DashboardResponse(BaseModel):
    total_users: int
    users_by_role: Dict[str, int]
    users_with_penalties: int
    total_resources: int
    resources_by_status: Dict[str, int]
    resources_by_lab: List[ResourceByLab]
    active_loans: int
    overdue_loans: int
    loans_by_status: Dict[str, int]
    total_printings_3d: int
    recent_loans: List[RecentLoanItem]
    top_penalty_users: List[PenaltyUserItem]
