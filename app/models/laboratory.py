from sqlalchemy import Column, BigInteger, Text
from sqlalchemy.orm import relationship
from app.database.session import Base


class Laboratory(Base):
    __tablename__ = "laboratories"

    id_laboratorio = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(Text, nullable=False, unique=True)

    resources = relationship("Resource", back_populates="laboratory")
    printers = relationship("Printer", back_populates="laboratory")
