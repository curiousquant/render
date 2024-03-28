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
import simulation
import numpy as np

templates = Jinja2Templates(directory="templates")

stock_router = APIRouter(
    prefix="/stocks", responses={400: {"description": "Not found"}}, tags=["auth"]
)


@stock_router.get("/")
async def stockhome(request: Request,
                    db:AsyncSession = Depends(db.get_session)):
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
        stmt = select(models.YFinanceNews,models.YFinanceScore,models.YFinanceStockPrice).outerjoin(models.YFinanceScore).outerjoin(models.YFinanceStockPrice,and_(models.YFinanceStockPrice.date==models.YFinanceNews.providerPublishTime,models.YFinanceStockPrice.ticker==models.YFinanceNews.ticker)).order_by(models.YFinanceStockPrice.date.desc())

        result = await session.execute(stmt)
        res = result.all()
        print(res)

        parms = {
            'X0' : 1,
            'theta' : .1,
            'mu' : .1,
            'sigma' : .1,
            'T':1,
            'num_steps' : 20,
            'num_sims':100
            }
        
        paths = simulation.gen_paths(**parms)
        x = list(range(paths.shape[0]))
        y = []
        for i in range(paths.shape[1]):
            y.append(list(paths[:,i]))
            
        print(res[0][2])
        tickers = []
        for i in range(len(res)):
            if not res[i][2] is None:
                tick = res[i][2].ticker
                if not tick in tickers:
                    tickers.append(tick)
        ystocks = []
        #tickers = ['MSFT']
        for ticker in tickers:
            stockprices =[]
            for i in range(len(res)):
                if not res[i][2]==None and res[i][2].ticker == ticker:
                    stockprice = res[i][2].price
                    stockprices.append(stockprice)
            ystocks.append(stockprices)
        xlabel_len =0
        for i in range(len(ystocks)):
            xlabel_len = max(xlabel_len,len(ystocks[i]))
        xlabel = list(range(xlabel_len))
        yzip = zip(ystocks,tickers)
    return templates.TemplateResponse("stocks.html",{"request":request,"dictdata":res,"y":y,"x": x,"yzip":yzip,"xlabel":xlabel})

@stock_router.post("/gen_path")
async def gen_path(request:Request,X0: float = Form(...),theta: float = Form(...),mu: float = Form(...),sigma: float = Form(...),T: float = Form(...),num_steps: int = Form(...),num_sims: int = Form(...),db:AsyncSession = Depends(db.get_session)):
    parms = {
            'X0' : X0,
            'theta' : theta,
            'mu' : mu,
            'sigma' : sigma,
            'T':T,
            'num_steps' : num_steps,
            'num_sims':num_sims
            }
    try:
        print("HI")
        paths = simulation.gen_paths(**parms)
        x = list(range(paths.shape[0]))
        y = []
        for i in range(paths.shape[1]):
            y.append(list(paths[:,i]))
        
        #print(x,y)
        #   print(paths)
            
    except Exception as e:
        print(e)
    
    return templates.TemplateResponse("vasicek.html",{"request":request,"x":x,"y":y})
@stock_router.get("/gen_path")
async def get_path(request:Request,db:AsyncSession = Depends(db.get_session)):
    parms = {
            'X0' : 1,
            'theta' : .1,
            'mu' : .1,
            'sigma' : .1,
            'T':1,
            'num_steps' : 5,
            'num_sims':5
            }
    try:
        print("HI")
        paths = simulation.gen_paths(**parms)
        x = list(range(paths.shape[0]))
        y = []
        for i in range(paths.shape[1]):
            y.append(list(paths[:,i]))
        
        #print(x,y)
        #   print(paths)
            
    except Exception as e:
        print(e)
    
    return templates.TemplateResponse("vasicek.html",{"request":request,"x":x,"y":y})

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
