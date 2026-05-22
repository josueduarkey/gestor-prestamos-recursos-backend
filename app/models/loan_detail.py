from sqlalchemy import Column, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class LoanDetail(Base):
    __tablename__ = "loan_details"

    id_detalle = Column(BigInteger, primary_key=True, autoincrement=True)
    id_loan = Column(BigInteger, ForeignKey("loans.id_loan"), nullable=False)
    id_recurso = Column(BigInteger, ForeignKey("resources.id_recurso"), nullable=False)
    cantidad = Column(Integer, nullable=False, default=1)

    loan = relationship("Loan", back_populates="loan_details")
    resource = relationship("Resource", back_populates="loan_details")
