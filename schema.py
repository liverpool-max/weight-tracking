from pydantic import BaseModel
from datetime import date

class UserCreateSchema(BaseModel):
    username :str
    password:str
    height:float
    class Config:
        extra = "forbid"


class WeightCreateSchema(BaseModel):
    username : str
    date : date
    class Config:
        extra = "forbid"