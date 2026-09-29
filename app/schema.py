from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional


# User Class

class User_Inherit(BaseModel):
    email : EmailStr


class User(User_Inherit):
    password : str


class Create_User_Response(User_Inherit):
 
    id : int
    created_at : datetime    
    model_config = ConfigDict(from_attributes=True)

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at : datetime
    owner_id : int
    owner : Create_User_Response
    class Config:
        from_attributes = True



class ResponsePost(BaseModel):
    message : str
    data : Post



#Auth

class User_credentials(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str 

class TokenData(BaseModel):
    id : Optional[int] = None



