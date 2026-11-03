import os
import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Загрузка переменных окружения при наличии
load_dotenv()

# Чтение конфигурационного файла config.ini
config = configparser.ConfigParser()
if os.path.exists("config.ini"):
    config.read("config.ini", encoding="utf-8")
    db_sec = config["database"] if "database" in config else {}
    DB_HOST = db_sec.get("host", "localhost")
    DB_PORT = db_sec.get("port", "5432")
    DB_NAME = db_sec.get("name", "session")
    DB_USER = db_sec.get("user", "postgres")
    DB_PASS = db_sec.get("password", "postgres")
else:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "session")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASSWORD", "postgres")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)
