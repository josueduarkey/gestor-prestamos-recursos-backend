from datetime import datetime, timezone
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.resource import Resource
from app.models.loan import Loan
from app.models.laboratory import Laboratory
from app.models.printing_3d import Printing3D


def _as_utc(dt: datetime) -> datetime:
    if dt is None:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def get_dashboard(self) -> dict:
        now = datetime.now(timezone.utc)

        role_rows = self.db.query(User.role, func.count(User.carnet)).group_by(User.role).all()
        users_by_role = {role: count for role, count in role_rows}
        total_users = sum(users_by_role.values())

        users_with_penalties = (
            self.db.query(func.count(User.carnet)).filter(User.penalizaciones > 0).scalar() or 0
        )
        top_penalty_users = (
            self.db.query(User).filter(User.penalizaciones > 0)
            .order_by(User.penalizaciones.desc()).limit(5).all()
        )

        status_rows = (
            self.db.query(Resource.estado, func.count(Resource.id_recurso))
            .group_by(Resource.estado).all()
        )
        resources_by_status = {(estado or "sin_estado"): count for estado, count in status_rows}
        total_resources = sum(resources_by_status.values())

        lab_rows = (
            self.db.query(
                Laboratory.nombre.label("laboratorio"),
                func.count(Resource.id_recurso).label("total"),
            )
            .outerjoin(Resource, Resource.id_laboratorio == Laboratory.id_laboratorio)
            .group_by(Laboratory.nombre).all()
        )

        loan_status_rows = (
            self.db.query(Loan.estado, func.count(Loan.id_loan)).group_by(Loan.estado).all()
        )
        loans_by_status = {estado: count for estado, count in loan_status_rows}
        active_loans = loans_by_status.get("activo", 0)

        overdue_list = (
            self.db.query(Loan)
            .filter(Loan.estado == "activo", Loan.fecha_limite.isnot(None))
            .all()
        )
        overdue_loans = sum(1 for l in overdue_list if _as_utc(l.fecha_limite) < now)

        recent_loans = (
            self.db.query(Loan).order_by(Loan.fecha_prestamo.desc()).limit(5).all()
        )

        total_printings_3d = self.db.query(func.count(Printing3D.id_impresion)).scalar() or 0

        return {
            "total_users": total_users,
            "users_by_role": users_by_role,
            "users_with_penalties": users_with_penalties,
            "total_resources": total_resources,
            "resources_by_status": resources_by_status,
            "resources_by_lab": [
                {"laboratorio": r.laboratorio, "total_recursos": r.total} for r in lab_rows
            ],
            "active_loans": active_loans,
            "overdue_loans": overdue_loans,
            "loans_by_status": loans_by_status,
            "total_printings_3d": total_printings_3d,
            "recent_loans": [
                {
                    "id_loan": l.id_loan,
                    "id_usuario": l.id_usuario,
                    "codigo_devolucion": l.codigo_devolucion,
                    "estado": l.estado,
                    "fecha_prestamo": l.fecha_prestamo,
                    "fecha_limite": l.fecha_limite,
                }
                for l in recent_loans
            ],
            "top_penalty_users": [
                {"carnet": u.carnet, "nombre": u.nombre, "penalizaciones": u.penalizaciones}
                for u in top_penalty_users
            ],
        }

    def get_overdue_loans_for_reminder(self) -> list[dict]:
        """Returns context dicts for each overdue loan — used for sending reminder emails."""
        from app.models.loan_detail import LoanDetail
        now = datetime.now(timezone.utc)
        overdue = (
            self.db.query(Loan)
            .filter(Loan.estado == "activo", Loan.fecha_limite.isnot(None))
            .all()
        )
        result = []
        for loan in overdue:
            if _as_utc(loan.fecha_limite) >= now:
                continue
            user = self.db.query(User).filter(User.carnet == loan.id_usuario).first()
            if not user:
                continue
            details = (
                self.db.query(LoanDetail).filter(LoanDetail.id_loan == loan.id_loan).all()
            )
            result.append({
                "correo": user.correo,
                "nombre": user.nombre,
                "carnet": user.carnet,
                "codigo_devolucion": loan.codigo_devolucion,
                "fecha_limite": loan.fecha_limite.strftime("%d/%m/%Y %H:%M") if loan.fecha_limite else "—",
                "recursos": [
                    {"nombre": d.resource.nombre, "codigo": d.resource.codigo, "cantidad": d.cantidad}
                    for d in details if d.resource
                ],
            })
        return result
