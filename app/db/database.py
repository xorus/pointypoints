from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.settings import settings

# SQLALCHEMY_DATABASE_URL = "sqlite:///./run/db.db"
SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA journal_mode=WAL")
#     cursor.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
