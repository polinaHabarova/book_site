from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATA_BASE_URL = 'sqlite:///./app.db'
engine = create_engine(DATA_BASE_URL, connect_args={"check_same_thread": False})
sessionLocal = sessionmaker(bind = engine, autoflush=False, autocommit=False)
Base = declarative_base()