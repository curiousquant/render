from fastapi import APIRouter

auth_router = APIRouter(
    prefix="/", responses={400: {"description": "Not found"}}, tags=["auth"]
)

@auth_router.get("/")
async def hello():
    """Hello home"""
    return {"message": "Hello Home"}
