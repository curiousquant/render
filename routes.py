from fastapi import APIRouter

routes = APIRouter(
    prefix="", responses={400: {"description": "Not found"}}, tags=["auth"]
)

@routes.get("/")
async def hello():
    """Hello home"""
    return {"message": "Hello Home"}
