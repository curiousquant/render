
from pydantic import BaseModel

class Users(BaseModel):
    id:int
    name:str

    class Config:
        orm_mode = True
        