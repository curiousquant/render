from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from config import settings



# class Base(DeclarativeBase):
#     pass
Base = declarative_base()

engine = create_engine(url=settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

def getdb():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


