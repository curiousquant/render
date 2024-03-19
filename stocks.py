
import yfinance as yf
import datetime
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

def readData(ticker:str,start:datetime=datetime.datetime(2021,1,1),end:datetime=datetime.datetime(2021,1,21)):
    d = yf.download(ticker,start,end)
    t = yf.Ticker(ticker)
    news = pd.DataFrame(t.news)
    print(news.columns)
    return news

def scoreData(df):
    res = {}
    index=0
    for i, row in df.iterrows():
        text = row['title']
        myid = index
        res[myid] = sia.polarity_scores(text)
        index+=1
    
    vaders = pd.DataFrame(res).T
    #vaders = vaders.reset_index()#.rename(columns={'index': 'Id'})
    vaders = pd.concat([df[['title','providerPublishTime','relatedTickers']],vaders],axis=1)
    return vaders

d=readData("MSFT")
print(scoreData(d))