from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# User
class UserBase(BaseModel):
    carnet: int
    nombre: str
    correo: str
    estado: Optional[str] = None
    penalizaciones: Optional[int] = None
    generacion: str
    role: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    class Config:
        from_attributes = True

# Laboratory
class LaboratoryBase(BaseModel):
    id_laboratorio: int
    nombre: str

class LaboratoryCreate(LaboratoryBase):
    pass

class LaboratoryResponse(LaboratoryBase):
    class Config:
        from_attributes = True

# Resource
class ResourceBase(BaseModel):
    id_recurso: int
    nombre: str
    categoria: Optional[str] = None
    codigo: Optional[str] = None
    cantidad_total: Optional[int] = None
    cantidad_disponible: Optional[int] = None
    estado: Optional[str] = None
    id_laboratorio: Optional[int] = None

class ResourceCreate(ResourceBase):
    pass

class ResourceResponse(ResourceBase):
    class Config:
        from_attributes = True

# Prestamo
class PrestamoBase(BaseModel):
    id_prestamo: int
    id_usuario: Optional[int] = None
    cantidad_prestado: Optional[int] = None
    codigo_devolucion: Optional[int] = None
    responsabilidad: Optional[bool] = None
    estado: Optional[bool] = None
    fecha_prestamo: Optional[datetime] = None

class PrestamoCreate(PrestamoBase):
    pass

class PrestamoResponse(PrestamoBase):
    class Config:
        from_attributes = True

# LoanDetail
class LoanDetailBase(BaseModel):
    id_detalle: int
    id_prestamo: Optional[int] = None
    id_recurso: Optional[int] = None

class LoanDetailCreate(LoanDetailBase):
    pass

class LoanDetailResponse(LoanDetailBase):
    class Config:
        from_attributes = True

# Return
class ReturnBase(BaseModel):
    id_devolucion: int
    id_prestamo: Optional[int] = None
    fecha_devolucion: Optional[datetime] = None
    estado: Optional[bool] = None
    evidencia: Optional[str] = None
    descripcion: Optional[str] = None
    responsabilidad: Optional[bool] = None

class ReturnCreate(ReturnBase):
    pass

class ReturnResponse(ReturnBase):
    class Config:
        from_attributes = True

# Material3D
class Material3DBase(BaseModel):
    id_material: int
    tipo_material: str
    Descripcion: str

class Material3DCreate(Material3DBase):
    pass

class Material3DResponse(Material3DBase):
    class Config:
        from_attributes = True

# Printing3D
class Printing3DBase(BaseModel):
    id_impresion: int
    id_prestamo: Optional[int] = None
    id_material: Optional[int] = None
    codigo_impresora: Optional[str] = None
    gramos: Optional[float] = None
    tiempo_estimado: Optional[int] = None
    tipo_trabajo: Optional[str] = None

class Printing3DCreate(Printing3DBase):
    pass

class Printing3DResponse(Printing3DBase):
    class Config:
        from_attributes = True