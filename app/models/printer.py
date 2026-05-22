from sqlalchemy import Column, BigInteger, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.database.session import Base


class Printer(Base):
    __tablename__ = "printers"

    id_printer = Column(BigInteger, primary_key=True, autoincrement=True)
    codigo = Column(Text, nullable=False, unique=True)
    nombre = Column(Text)
    estado = Column(Text, default="disponible")
    id_laboratorio = Column(BigInteger, ForeignKey("laboratories.id_laboratorio"))

    laboratory = relationship("Laboratory", back_populates="printers")
    printings = relationship("Printing3D", back_populates="printer")

    __table_args__ = (Index("ix_printers_laboratorio", "id_laboratorio"),)
