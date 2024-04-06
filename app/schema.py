from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
class POST(BaseModel):
    title:str
    content:str
    description:str



class POST_Create(POST):
    pass

class POST_Update(POST):
    pass 

class User_Response(BaseModel):
    username:str
    user_id:int
    description:Optional[str]
    name:str

    class Config:
        orm_mode = True    

class POST_Response(POST):
    created_at:datetime
    user:User_Response
    class Config:
        orm_mode = True


class User(BaseModel):
    username:str
    password : str
    description:Optional[str]
    phone:str
    email:EmailStr
    name:str



class Userlogin(BaseModel):
    username:str
    password:str
    



class comment(BaseModel):
    comment:str


class token(BaseModel):
    access_token :str
    token_type :str
    class Config:
        orm_mode = True

class tokendata(BaseModel):
    id:str          

