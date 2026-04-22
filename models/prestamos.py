from sqlalchemy import Column, Integer, ForeignKey, String, DateTime

class Prestamo():
    __tablename__ = "prestamos"

    id_prestamo = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    estado = Column(String)
    fecha_prestamo = Column(DateTime)
