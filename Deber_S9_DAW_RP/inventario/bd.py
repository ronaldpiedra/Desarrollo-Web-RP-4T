import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .productos import Base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "inventario.db")

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    return SessionLocal()