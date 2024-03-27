from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, DateTime, Double, ForeignKey, UniqueConstraint
from uuid import uuid4
from datetime import datetime
from db import Base
from sqlalchemy import Column,Integer,String, Sequence
from sqlalchemy.orm import relationship

class User(Base):
    """
    The users' auth model
    """

    __tablename__ = "users"
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4()
    )
    username: Mapped[str] = mapped_column(nullable=True)
    first_name:Mapped[str] = mapped_column(nullable=True)
    last_name:Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    verified: Mapped[bool] = mapped_column(default=False)

    def __str__(self):
        return f"<User {self.email}>"

class Users(Base):
    __tablename__ = "user"

    id = Column(Integer,primary_key=True)
    name = Column(String)
    
class Headlines(Base):
    __tablename__ = "headline"
    id = Column(Integer,primary_key=True)
    title = Column(String,unique=True)
    published_date = Column(DateTime(timezone=True))

class Score(Base):
    __tablename__="score"
    id = Column(Integer,ForeignKey(Headlines.id),primary_key=True)
    neg = Column(Double)
    pos = Column(Double)
    neu = Column(Double)
    compound = Column(Double)
    
# class Address(Base):
#     __tablename__ = "addresses"
#     id = Column(Integer,primary_key=True)
#     user_id = Column(Integer,ForeignKey("user.id"))
#     address = Column(String)
#     users = relationship("User",back_populates="addresses")

class YFinanceNews(Base):
    __tablename__="yfinancenews"
    id = Column(Integer,primary_key=True)
    ticker=Column(String)
    title=Column(String,unique=True)
    relatedTickers=Column(String)
    providerPublishTime=Column(DateTime(timezone=True))

class YFinanceScore(Base):
    __tablename__="yfinancescore"
    id = Column(Integer,ForeignKey(YFinanceNews.id),primary_key=True)
    neg = Column(Double)
    neu = Column(Double)
    pos = Column(Double)
    compound = Column(Double)

class YFinanceStockPrice(Base):
    __tablename__="yfinancestockprice"  
    __table_args__ = (UniqueConstraint('ticker', 'date'),)

    id = Column(Integer,primary_key=True)
    ticker = Column(String,)
    date = Column(DateTime(timezone=True))
    price = Column(Double)    

class Vasicek(Base):
    __tablename__="vasicek"
    id = Column(Integer,primary_key=True)
    date = Column(Integer)
    rate = Column(Double)
    