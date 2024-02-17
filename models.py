from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, ForeignKey
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
    
# class Address(Base):
#     __tablename__ = "addresses"
#     id = Column(Integer,primary_key=True)
#     user_id = Column(Integer,ForeignKey("user.id"))
#     address = Column(String)
#     users = relationship("User",back_populates="addresses")



