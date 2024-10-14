from models import User,Weight
from schema import *
from sqlalchemy.orm import Session
from exception import UserNotFoundException
import psycopg2
from settings import DATABASE_URL
import bcrypt
from fastapi import HTTPException
from datetime import datetime


def get_user_from_db(*,username:str, db: Session):
    user = db.query(User).filter(User.username==username).first()
    if not user:
        raise UserNotFoundException()
    lst = []
    weights = db.query(Weight).filter_by(username=user.username,weight=Weight.weight).all()
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
    return {"Message":"new user is created"}


def create_weight_in_db(*,username:str, data: WeightCreateSchema, db : Session):
    new_weight = Weight(username=username,weight=data.weigth,datetime=data.datetime)
    user=db.query(User).filter(User.username == new_weight.username).first()
    if not user:
        raise UserNotFoundException
    lst = []
    weights = db.query(Weight).filter_by(username=user.username,weight=Weight.weight).all()
    lst.append(weights)
    if len(lst[0]) == 0 :
        db.add(new_weight)
        db.commit()
        db.refresh(new_weight)
    else:
        last_entry = lst[0][-1]
    last = last_entry
    if last.datetime == data.datetime:
        a=db.query(Weight).filter_by(username = username).update({"weight":new_weight.weight})
        db.commit()
        return {"msg":"weight updated"}
    else:
        db.add(new_weight)
        db.commit()
        db.refresh(new_weight)
    

def get_weight_change_from_db(*,username:str, db: Session):
    user = db.query(Weight).filter(Weight.username==username).first()
    if not user:
        raise UserNotFoundException()
    lst = []
    weights = db.query(Weight).filter_by(username=user.username,weight=Weight.weight).all()
    lst.append(weights)
    last_entry = lst[0][-1]
    if len(lst[0])!=1:
        first_entry = lst[0][0].weight
    else:
        raise HTTPException(status_code=404,detail="User entered only one weight")
    a = abs(last_entry.weight-first_entry)
    if a > 0:
        return {f"Message: You get fat {a} kg and your weight: {last_entry.weight}"}
    else:
        return {f"Message: You lose weight {a} kg and your weight: {last_entry.weight}"}


def calculate_bmi_for_last_weight(*,username:str, db: Session):
    user = db.query(User).filter(User.username==username).first()
    if not user:
        raise UserNotFoundException()
    lst = []
    weights = db.query(Weight).filter_by(username=user.username,weight=Weight.weight).all()
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
