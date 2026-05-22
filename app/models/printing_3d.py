from datetime import datetime, timezone
from sqlalchemy import Column, BigInteger, Float, Integer, Text, ForeignKey, TIMESTAMP, Index
from sqlalchemy.orm import relationship
from app.database.session import Base


class Printing3D(Base):
    __tablename__ = "printings_3d"

    id_impresion = Column(BigInteger, primary_key=True, autoincrement=True)
    id_usuario = Column(BigInteger, ForeignKey("users.carnet"), nullable=False)
    id_printer = Column(BigInteger, ForeignKey("printers.id_printer"), nullable=False)
    id_material = Column(BigInteger, ForeignKey("materials_3d.id_material"), nullable=False)
    gramos = Column(Float)
    tiempo_estimado = Column(Integer)
    tipo_trabajo = Column(Text)
    estado = Column(Text, default="pendiente")
    fecha_solicitud = Column(TIMESTAMP(timezone=True))

    user = relationship("User", back_populates="printings")
    printer = relationship("Printer", back_populates="printings")
    material = relationship("Material3D", back_populates="printings")

    __table_args__ = (Index("ix_printings_usuario", "id_usuario"),)
