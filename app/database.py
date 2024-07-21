import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = (f"postgresql://{os.getenv('POSTGRES_USER', 'postgres')}:"
                           f"{os.getenv('POSTGRES_PASSWORD', 'postgres')}@"
                           f"{os.getenv('POSTGRES_HOST', 'localhost')}/{os.getenv('POSTGRES_DATABASE', 'postgres')}")
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
