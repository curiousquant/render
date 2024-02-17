from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.orm import Session
import db
import models
import schemas
from sqlalchemy.ext.asyncio import AsyncSession

routes = APIRouter(
    prefix="", responses={400: {"description": "Not found"}}, tags=["auth"]
)

@routes.get("/")
async def hello():
    """Hello home"""
    return {"message": "Hello Home"}


@routes.get("/users")
async def read_item(db:AsyncSession = Depends(db.get_session)):
    async with db() as session:
        stmt = select(models.Users)
        result = await session.execute(stmt)
        getter = await session.get(models.Users,[1])

    return result.scalars().all()
@routes.get("/users/{userid}")
async def read_user(userid:int,db:AsyncSession = Depends(db.get_session)):
    async with db() as session:
        stmt = select(models.Users).where(models.Users.id==userid)
        result = await session.execute(stmt)

    return result.scalars().all()

@routes.post("/users")
async def postuser(user:schemas.Users,db:AsyncSession = Depends(db.get_session)):
    print(user)
    async with db() as session:
        name = user.name
        session.add(models.Users(name=name))
        await session.commit()
    return user
