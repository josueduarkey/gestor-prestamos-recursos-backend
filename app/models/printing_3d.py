from sqlalchemy import Column, BigInteger, Float, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class Printing3D(Base):
    __tablename__ = "printings_3d"

    id_impresion = Column(BigInteger, primary_key=True, autoincrement=True)
    id_loan = Column(BigInteger, ForeignKey("loans.id_loan"), nullable=False, unique=True)
    id_material = Column(BigInteger, ForeignKey("materials_3d.id_material"), nullable=False)
    codigo_impresora = Column(Text, nullable=False)
    gramos = Column(Float)
    tiempo_estimado = Column(Integer)
    tipo_trabajo = Column(Text)

    loan = relationship("Loan", back_populates="printing_3d")
    material = relationship("Material3D", back_populates="printings")
