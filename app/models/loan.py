from sqlalchemy import Column, BigInteger, Boolean, TIMESTAMP, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.database.session import Base


class Loan(Base):
    __tablename__ = "loans"

    id_loan = Column(BigInteger, primary_key=True, autoincrement=True)
    id_usuario = Column(BigInteger, ForeignKey("users.carnet"), nullable=False)
    codigo_devolucion = Column(Text, unique=True, nullable=False)
    responsabilidad = Column(Boolean, default=False)
    estado = Column(Text, default="activo")
    fecha_prestamo = Column(TIMESTAMP(timezone=True))
    fecha_limite = Column(TIMESTAMP(timezone=True))

    user = relationship("User", back_populates="loans")
    loan_details = relationship("LoanDetail", back_populates="loan", cascade="all, delete-orphan")
    return_ = relationship("Return", back_populates="loan", uselist=False)
    printing_3d = relationship("Printing3D", back_populates="loan", uselist=False)

    __table_args__ = (
        Index("ix_loans_usuario", "id_usuario"),
        Index("ix_loans_estado", "estado"),
    )
