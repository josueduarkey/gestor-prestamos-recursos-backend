from sqlalchemy import Column, BigInteger, Integer, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.database.session import Base


class Resource(Base):
    __tablename__ = "resources"

    id_recurso = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(Text, nullable=False)
    categoria = Column(Text)
    codigo = Column(Text, unique=True)
    cantidad_total = Column(Integer, default=0)
    cantidad_disponible = Column(Integer, default=0)
    estado = Column(Text, default="disponible")
    imagen = Column(Text)
    id_laboratorio = Column(BigInteger, ForeignKey("laboratories.id_laboratorio"))

    laboratory = relationship("Laboratory", back_populates="resources")
    loan_details = relationship("LoanDetail", back_populates="resource")

    __table_args__ = (
        Index("ix_resources_estado", "estado"),
        Index("ix_resources_laboratorio", "id_laboratorio"),
    )
