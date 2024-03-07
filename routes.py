from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request, FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session
import db
import models
import schemas
import sentiment
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

templates = Jinja2Templates(directory="templates")

routes = APIRouter(
    prefix="", responses={400: {"description": "Not found"}}, tags=["auth"]
)

async def read_item(request:Request,db:AsyncSession = Depends(db.get_session)):
    async with db() as session:
        stmt = select(models.Users)
        result = await session.execute(stmt) 

    return templates.TemplateResponse("users.html",{"request":request,"name":"First Last","result":result.scalars().all()})



@routes.get("/")
async def home(request: Request,db:AsyncSession = Depends(db.get_session)):
    """Hello home"""
    #dogs = [{"name":"Milo","type":"Golden Retriever"},{"name":"Jax","type":"German Shepard"}]
    #data = sentiment.readSite()
    #df = sentiment.scoredf(data)
    #print(df.head())
    #dictdata = df.to_dict('records')
    #print(dictdata)
    async with db() as session:
        stmt = select(models.Headlines)
        result = await session.execute(stmt) 
        stmt2 = select(models.Score)
        result2 = await session.execute(stmt2)
        result = result.scalars().all()
        result2 = result2.scalars().all()
        #print((result))

        stmt = select(models.Headlines,models.Score).join(models.Score)
        result = await session.execute(stmt)
        res = result.all()

    return templates.TemplateResponse("index.html",{"request":request,"name":"title compound","dictdata":res})

@routes.post("/")
async def refresh(request:Request, db:AsyncSession = Depends(db.get_session)):
    data = sentiment.readSite()
    df = sentiment.scoredf(data)
    async with db() as session:
        for i in range(len(df)):
            title = df.loc[i,'title']
            time = df.loc[i,'published_date']
            neg = df.loc[i,'neg']
            pos = df.loc[i,'pos']
            neu = df.loc[i,'neu']
            compound = df.loc[i,'compound']
            published_date = datetime.strptime(time,'%Y-%m-%dT%H:%M:%S%z')
            try:
                m = models.Headlines(title=title,published_date=published_date)
                session.add(m)
                await session.commit()
            
                session.add(models.Score(id=m.id,neg=neg,pos=pos,neu=neu,compound=compound))
                await session.commit()

                
            except Exception as e:
                print(e)

    redirect_url = request.url_for('home')
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER) 

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
