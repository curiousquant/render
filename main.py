from typing import List
from fastapi import FastAPI,Depends,Request
import uvicorn
from db import Base, engine, SessionLocal
import models
import db
import schemas
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/users/")
def read_item(db:Session = Depends(db.getdb)):
    records = db.query(models.Users).order_by(models.Users.id).all()
    for instance in db.query(models.Users).order_by(models.Users.name).all():
        print(instance.id,instance.name)
    return records

@app.get("/users/{userid}")
def readuser(userid:str, request:Request,db:Session = Depends(db.getdb)):
    record = db.query(models.Users).filter_by(name=userid).order_by(models.Users.id).first()
    return record

@app.post("/users")
async def postuser(user:schemas.Users,db:Session = Depends(db.getdb)):
    print(user)
    name = user.name
    db.add(models.Users(name=name))
    db.commit()
    return user

@app.get("/address")
async def getaddress(db:Session=Depends(db.getdb)):
    print(models.Users)
    records = db.query(models.Users).first()
    
    print(records)
    return records

@app.get("/address/{userid}")
async def getuseraddress(userid:str,db:Session=Depends(db.getdb)):
    record = db.query(models.Address).filter_by(user_id=userid)
    return record
if __name__=='__main__':
    uvicorn.run("main:app", reload=True)