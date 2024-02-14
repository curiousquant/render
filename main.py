from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from auth import AuthHandler
from schema import AuthDetails
import uvicorn


app = FastAPI()
templates = Jinja2Templates(directory="templates")

auth_handler = AuthHandler()
users = []
dogs = [{"type":"german shepard","name":"Bob"},{"type":"german shepard","name":"Bob2"}]
@app.get("/")
async def name(request:Request):
    return templates.TemplateResponse("index.html",{"request":request,"name":"coding","dogs":dogs})

@app.post("/register")
def register(auth_details:AuthDetails):
    if any(x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({
        'username': auth_details.username,
        'password': hashed_password    
    })

@app.post('/login')
def login(auth_details: AuthDetails):
    user = None
    for x in users:
        if x['username'] == auth_details.username:
            user = x
            break
    
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return { 'token': token }


@app.get('/unprotected')
def unprotected():
    return { 'hello': 'world' }


@app.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    print(username) 
    return { 'name': username }

if __name__=='__main__':
    uvicorn.run("main:app", reload=True)