from fastapi import FastAPI
import uvicorn
from auth_routes import auth_router
from routes import routes
from config import Settings
from contextlib import asynccontextmanager
from config import settings
from db import init_db




# lifespan code

@asynccontextmanager
async def lifespan(app:FastAPI):
    import nltk
    nltk.download('vader_lexicon')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')
    await init_db()
    
    yield

def create_app():
    app = FastAPI(
        description="This is a simple REST API for a book review service",
        title="Bookly",
        version=settings.VERSION,
        lifespan=lifespan
    )
    app.include_router(auth_router)
    app.include_router(routes)
    return app


app = create_app()

if __name__=='__main__':
    uvicorn.run("__init__:app", reload=True)