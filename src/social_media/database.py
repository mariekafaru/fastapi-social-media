from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from src.social_media.config import settings

DATABASE_URL = (
    f"postgresql+psycopg2://{settings.database_username}:"
    f"{settings.database_password}@"
    f"{settings.database_hostname}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
)

engine = create_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DATABASE_URL = "postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{database.hostname}:{settings.database_port}/{settings.database_name}"



