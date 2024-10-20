from models import User,Weight
from schema import *
from sqlalchemy.orm import Session
from exception import UserNotFoundException, WeightNotFoundException
import psycopg2
from settings import DATABASE_URL
import bcrypt
from fastapi import HTTPException,Query
from datetime import datetime


def get_user_from_db(*,username:str, db: Session):
    user = db.query(User).filter(User.username==username).first()
    if not user:
        raise UserNotFoundException()
    lst = []
    weights = db.query(Weight).filter_by(username=user.username,weight=Weight.weight).order_by(Weight.datetime).all()
    if not weights:
        raise WeightNotFoundException
    lst.append(weights)
    last_entry = lst[0][-1]
    return {"username":user.username,"weight":last_entry.weight}


def create_user_in_db(*,data: UserCreateSchema,db:Session):
    hashed_password=bcrypt.hashpw(data.password.encode("utf-8"),bcrypt.gensalt())
    new_user=User(username=data.username,password=hashed_password.decode("utf-8"),height=data.height)
    user=db.query(User).filter_by(username=new_user.username).first()
    if user:
        raise UserNotFoundException
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"Message":"New user is created"}


def create_new_weight(weight:int,data:WeightCreateSchema,db:Session):
    user = db.query(User).filter(User.username==data.username).first()
    if not user:
        raise UserNotFoundException()
    existing_weight = db.query(Weight).filter(Weight.username == data.username,Weight.datetime == data.date).first()
    if existing_weight:
        existing_weight.weight = weight
        db.commit()
        return {"Message": "Weight is updated"}
    else:
        new_weight=Weight(username=data.username,weight=weight,datetime=data.date)
        db.add(new_weight)
        db.commit()
        db.refresh(new_weight)
        return {"Message":"New weight is created"}
    

def get_weight_change_from_db(*,username:str, db: Session):
    user = db.query(User).filter(User.username==username).first()
    if not user:
        raise UserNotFoundException()
    lst = []
    weights = db.query(Weight).filter_by(username=user.username,weight=Weight.weight).order_by(Weight.datetime).all()
    if not weights:
        raise WeightNotFoundException
    lst.append(weights)
    last_entry = lst[0][-1]
    if len(lst[0])!=1:
        first_entry = lst[0][0].weight
    else:
        raise HTTPException(status_code=404,detail="User entered only one weight")
    a = abs(last_entry.weight-first_entry)
    if last_entry.weight == first_entry:
        return {f"Message: Your weight has not changed and your weight {last_entry.weight}"}
    elif last_entry.weight > first_entry:
        return {f"Message: You get fat {a} kg and your weight: {last_entry.weight}"}
    elif last_entry.weight < first_entry:
        return {f"Message: You lose {a} kg and your weight: {last_entry.weight}"}


def calculate_bmi_for_last_weight(*,username:str, db: Session):
    user = db.query(User).filter(User.username==username).first()
    if not user:
        raise UserNotFoundException()
    lst = []
    weights = db.query(Weight).filter_by(username=user.username,weight=Weight.weight).order_by(Weight.datetime).all()
    if not weights:
        raise WeightNotFoundException
    lst.append(weights)
    last_entry = lst[0][-1]
    heights= db.query(User).filter_by(username = user.username, height = User.height).first()
    height1 = heights.height
    BMI = last_entry.weight/height1**2
    if BMI < 18:
        return {f"Message: Your BMI: {BMI} and you are underweight"}
    elif BMI < 25:
        return {f"Message: Your BMI: {BMI} and you are normal"}
    elif BMI < 30:
        return {f"Message: Your BMI: {BMI} and you are overweight"}
    else: 
        return {f"Message: Your BMI: {BMI} and you are obesity"}

