from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request, FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import and_, select
from sqlalchemy.orm import Session
import db
import models
import schemas
import stocks
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


templates = Jinja2Templates(directory="templates")

stock_router = APIRouter(
    prefix="/stocks", responses={400: {"description": "Not found"}}, tags=["auth"]
)


@stock_router.get("/")
async def stockhome(request: Request,db:AsyncSession = Depends(db.get_session)):
    """Hello home"""
    #dogs = [{"name":"Milo","type":"Golden Retriever"},{"name":"Jax","type":"German Shepard"}]
    #data = sentiment.readSite()
    #df = sentiment.scoredf(data)
    #print(df.head())
    #dictdata = df.to_dict('records')
    #print(dictdata)
    async with db() as session:
        stmt = select(models.YFinanceNews)
        result = await session.execute(stmt) 
        stmt2 = select(models.YFinanceScore)
        result2 = await session.execute(stmt2)
        result = result.scalars().all()
        result2 = result2.scalars().all()
        #print((result))
    
        stmt = select(models.YFinanceNews,models.YFinanceScore).join(models.YFinanceScore)
        stmt = select(models.YFinanceNews,models.YFinanceScore,models.YFinanceStockPrice).join(models.YFinanceScore).outerjoin(models.YFinanceStockPrice,and_(models.YFinanceStockPrice.date==models.YFinanceNews.providerPublishTime,models.YFinanceStockPrice.ticker==models.YFinanceNews.ticker))

        result = await session.execute(stmt)
        res = result.all()
        print(res)
        
    return templates.TemplateResponse("stocks.html",{"request":request,"name":"title compound","dictdata":res})


@stock_router.post("/")
async def refresh(request:Request,ticker: str = Form(...), db:AsyncSession = Depends(db.get_session)):
    data = stocks.readData(ticker)
    df = stocks.scoreData(data)
    stock = stocks.getPrice(ticker)
    async with db() as session:
        for i in range(len(df)):
            title = df.loc[i,'title']
            time = df.loc[i,'providerPublishTime']
            print(time)
            relatedTickers = ",".join(df.loc[i,'relatedTickers'])
            neg = df.loc[i,'neg']
            pos = df.loc[i,'pos']
            neu = df.loc[i,'neu']
            compound = df.loc[i,'compound']
            published_date = datetime(*datetime.fromtimestamp(time).timetuple()[:3]) 
            stockDate = datetime(*datetime.now().timetuple()[:3])
            stockPrice = stock
            try:
                m = models.YFinanceNews(title=title,ticker=ticker,providerPublishTime=published_date,relatedTickers=relatedTickers)
                session.add(m)
                await session.commit()
            
                session.add(models.YFinanceScore(id=m.id,neg=neg,pos=pos,neu=neu,compound=compound))
                await session.commit()

                session.add(models.YFinanceStockPrice(ticker=ticker,date=stockDate,price=stockPrice))
                await session.commit()

            except Exception as e:
                print(e)

    redirect_url = request.url_for('stockhome')
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER) 
