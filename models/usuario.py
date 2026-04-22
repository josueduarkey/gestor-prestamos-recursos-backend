from sqlalchemy import Column, Integer, String


class Usuario():
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    correo = Column(String, unique=True)
    estado = Column(String)
2