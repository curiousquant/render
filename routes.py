from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request, FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session
import db
import models
import schemas
from sqlalchemy.ext.asyncio import AsyncSession

templates = Jinja2Templates(directory="templates")

routes = APIRouter(
    prefix="", responses={400: {"description": "Not found"}}, tags=["auth"]
)

@routes.get("/")
async def hello(request: Request):
    """Hello home"""
    dogs = [{"name":"Milo","type":"Golden Retriever"},{"name":"Jax","type":"German Shepard"}]
    return templates.TemplateResponse("index.html",{"request":request,"name":"First Last","dogs":dogs})


@routes.get("/users")
async def read_item(request:Request,db:AsyncSession = Depends(db.get_session)):
    async with db() as session:
        stmt = select(models.Users)
        result = await session.execute(stmt) 

    return templates.TemplateResponse("users.html",{"request":request,"name":"First Last","result":result.scalars().all()})

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

@routes.post("/submit/")
async def submit(request:Request,nm: str = Form(...),db:AsyncSession = Depends(db.get_session)):
    async with db() as session:
        name = nm
        session.add(models.Users(name=name))
        await session.commit()

    redirect_url = request.url_for('read_item')
    print(redirect_url)
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER) 

@routes.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}
