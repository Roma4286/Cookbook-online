from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import registry
from sqlalchemy import create_engine, MetaData

from server.config import settings

engine = create_engine(settings.db_url)

metadata = MetaData()

mapper_registry = registry()
Base = mapper_registry.generate_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
