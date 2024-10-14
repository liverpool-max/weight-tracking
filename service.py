from models import User,Weight
from schema import *
from sqlalchemy.orm import Session
from exception import UserNotFoundException
import psycopg2
from settings import DATABASE_URL
import bcrypt


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
    db.add(new_weight)
    db.commit()
    db.refresh(new_weight)
    return {"Message":"new weight is created"}


    