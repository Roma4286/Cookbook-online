from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import registry
from sqlalchemy import create_engine

from config import settings

engine = create_engine(settings.db_url)

mapper_registry = registry()
Base = mapper_registry.generate_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
