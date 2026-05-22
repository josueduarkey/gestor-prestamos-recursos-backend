from sqlalchemy import Column, BigInteger, Boolean, TIMESTAMP, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class Return(Base):
    __tablename__ = "returns"

    id_devolucion = Column(BigInteger, primary_key=True, autoincrement=True)
    id_loan = Column(BigInteger, ForeignKey("loans.id_loan"), nullable=False, unique=True)
    fecha_devolucion = Column(TIMESTAMP(timezone=True))
    estado = Column(Text, default="completado")
    evidencia = Column(Text)
    descripcion = Column(Text)
    hay_danios = Column(Boolean, default=False)

    loan = relationship("Loan", back_populates="return_")
