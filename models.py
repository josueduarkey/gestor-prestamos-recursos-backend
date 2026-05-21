from sqlalchemy import Column, BigInteger, String, Boolean, Integer, Float, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    carnet = Column(BigInteger, primary_key=True)
    nombre = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    correo = Column(Text, nullable=False, unique=True)
    estado = Column(Text)
    penalizaciones = Column(Integer)
    generacion = Column(Text, nullable=False)
    role = Column(Text, nullable=False)

    prestamos = relationship("Prestamo", back_populates="usuario")

class Laboratory(Base):
    __tablename__ = "laboratories"
    id_laboratorio = Column(BigInteger, primary_key=True)
    nombre = Column(Text, nullable=False)

    resources = relationship("Resource", back_populates="laboratorio")

class Resource(Base):
    __tablename__ = "resources"
    id_recurso = Column(BigInteger, primary_key=True)
    nombre = Column(Text, nullable=False)
    categoria = Column(Text)
    codigo = Column(Text, unique=True)
    cantidad_total = Column(Integer)
    cantidad_disponible = Column(Integer)
    estado = Column(Text)
    id_laboratorio = Column(BigInteger, ForeignKey("laboratories.id_laboratorio"))

    laboratorio = relationship("Laboratory", back_populates="resources")
    loan_details = relationship("LoanDetail", back_populates="recurso")

class Prestamo(Base):
    __tablename__ = "prestamos"
    id_prestamo = Column(BigInteger, primary_key=True)
    id_usuario = Column(BigInteger, ForeignKey("users.carnet"))
    cantidad_prestado = Column(BigInteger)
    codigo_devolucion = Column(BigInteger)
    responsabilidad = Column(Boolean)
    estado = Column(Boolean)  # True = activo, False = finalizado
    fecha_prestamo = Column(TIMESTAMP(timezone=True))

    usuario = relationship("User", back_populates="prestamos")
    loan_details = relationship("LoanDetail", back_populates="prestamo")
    returns = relationship("Return", back_populates="prestamo", uselist=False)
    printing_3d = relationship("Printing3D", back_populates="prestamo", uselist=False)

class LoanDetail(Base):
    __tablename__ = "loan_details"
    id_detalle = Column(BigInteger, primary_key=True)
    id_prestamo = Column(BigInteger, ForeignKey("prestamos.id_prestamo"))
    id_recurso = Column(BigInteger, ForeignKey("resources.id_recurso"))

    prestamo = relationship("Prestamo", back_populates="loan_details")
    recurso = relationship("Resource", back_populates="loan_details")

class Return(Base):
    __tablename__ = "returns"
    id_devolucion = Column(BigInteger, primary_key=True)
    id_prestamo = Column(BigInteger, ForeignKey("prestamos.id_prestamo"))
    fecha_devolucion = Column(TIMESTAMP(timezone=True))
    estado = Column(Boolean)
    evidencia = Column(Text)
    descripcion = Column(Text)
    responsabilidad = Column(Boolean)

    prestamo = relationship("Prestamo", back_populates="returns")

class Material3D(Base):
    __tablename__ = "material_3D"
    id_material = Column(BigInteger, primary_key=True)
    tipo_material = Column(Text, nullable=False)
    Descripcion = Column(Text, nullable=False)

    printing_3d = relationship("Printing3D", back_populates="material")

class Printing3D(Base):
    __tablename__ = "printing_3d"
    id_impresion = Column(BigInteger, primary_key=True)
    id_prestamo = Column(BigInteger, ForeignKey("prestamos.id_prestamo"))
    id_material = Column(BigInteger, ForeignKey("material_3D.id_material"))
    codigo_impresora = Column(Text)
    gramos = Column(Float)
    tiempo_estimado = Column(Integer)
    tipo_trabajo = Column(Text)

    prestamo = relationship("Prestamo", back_populates="printing_3d")
    material = relationship("Material3D", back_populates="printing_3d")