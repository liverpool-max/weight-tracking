from fastapi import FastAPI,Depends,Query
from db import get_db
from sqlalchemy.orm import Session
from schema import *
from service import *

app = FastAPI()


@app.get("/user")
def get_user(username: str, db: Session = Depends(get_db)):
    message = get_user_from_db(username = username, db = db)
    return message

@app.post("/user")
def create_user(item : UserCreateSchema, db:Session = Depends(get_db)):
    message = create_user_in_db(data=item,db=db)
    return message

@app.post("/weight")
def create_weight(weight:float,item : WeightCreateSchema, db:Session = Depends(get_db)):
    message = create_new_weight(weight=weight,data=item,db=db)
    return message

@app.get("/weight_diff")
def different_weight(username: str, db: Session = Depends(get_db)):
    message = get_weight_change_from_db(username = username, db = db)
    return message

@app.get("/weight")
def calculate_bmi(username: str, db: Session = Depends(get_db)):
    message = calculate_bmi_for_last_weight(username = username, db = db)
    return message


