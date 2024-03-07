#https://www.kaggle.com/code/robikscube/sentiment-analysis-python-youtube-tutorial

import pandas as pd
# import nltk
# nltk.download('vader_lexicon')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm.notebook import tqdm
import requests
from config import settings

sia = SentimentIntensityAnalyzer()

def readSite():
    key = settings.API_KEY
    x = requests.get('https://api.nytimes.com/svc/topstories/v2/home.json?api-key='+key)
    df = pd.DataFrame(x.json()['results'])
    
    print(df.head())
    return df

def readcsv(file):
    df = pd.read_csv(file)
    # Read in data
    print(df.shape)
    return df


def scoredf(df):
    
    res = {}
    index=0
    for i, row in df.iterrows():
        text = row['title']
        myid = index
        res[myid] = sia.polarity_scores(text)
        index+=1
    
    vaders = pd.DataFrame(res).T
    #vaders = vaders.reset_index()#.rename(columns={'index': 'Id'})
    vaders = pd.concat([df[['title','published_date']],vaders],axis=1)
    return vaders

#df = readcsv('./input/Reviews.csv')

df = readSite()
df = scoredf(df)
print(df.to_json('temp.json', orient='records', lines=True))
