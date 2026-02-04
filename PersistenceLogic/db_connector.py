import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv("config/.env")
postgres_url = f"postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv('DB_HOST')}:{os.getenv("DB_PORT")}/{os.getenv('DB_NAME')}"
sqlite = f"sqlite:///./books.db"

DB_URL = postgres_url

# Creazione dell'engine per la gestione dei pool di connessione
engine = create_engine(DB_URL)

# Generatore di sessione
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()