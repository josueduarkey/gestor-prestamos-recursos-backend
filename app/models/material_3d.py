from sqlalchemy import Column, BigInteger, Text
from sqlalchemy.orm import relationship
from app.database.session import Base


class Material3D(Base):
    __tablename__ = "materials_3d"

    id_material = Column(BigInteger, primary_key=True, autoincrement=True)
    tipo_material = Column(Text, nullable=False)
    descripcion = Column(Text)

    printings = relationship("Printing3D", back_populates="material")
