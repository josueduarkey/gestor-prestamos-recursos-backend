from sqlalchemy import Column, BigInteger, Integer, Text
from sqlalchemy.orm import relationship
from app.database.session import Base


class User(Base):
    __tablename__ = "users"

    carnet = Column(BigInteger, primary_key=True)
    nombre = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    correo = Column(Text, nullable=False, unique=True)
    estado = Column(Text, default="activo")
    penalizaciones = Column(Integer, default=0)
    generacion = Column(Text, nullable=False)
    role = Column(Text, nullable=False)

    loans = relationship("Loan", back_populates="user")
