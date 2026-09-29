
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter

from app.database import get_db

from app.schema import Create_User_Response,User

from app.model import User as user_table
from app import utils

router = APIRouter(prefix="/user",tags=["User"])

@router.post("/", response_model=Create_User_Response )
def post_user(user : User , db:Session = Depends(get_db) ):

    #  new_password = password_user.hash(user.password)
    #  user.password = new_password
    hashed_password = utils.hash_password(user.password)
    create_user_table = user_table(email=user.email, password=hashed_password)

    db.add(create_user_table)
    db.commit()
    db.refresh(create_user_table)
    return create_user_table

@router.get("/{id}" ,response_model=Create_User_Response )
def get_user(id : int,db:Session = Depends(get_db)):
    get_user_id = db.query(user_table).filter(user_table.id == id).first()
    return get_user_id

