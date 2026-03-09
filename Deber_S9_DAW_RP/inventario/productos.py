from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(120), nullable=False)
    precio = Column(Float, nullable=False)
    cantidad = Column(Integer, nullable=False)