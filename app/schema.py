from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional,Any
class POST(BaseModel):
    title:str
    content:str
    description:Optional[str]

class login(BaseModel):
    username:str
    password:str


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
    post_id:int
    created_at:Any
    username:str
    user_id:int
    class Config:
        orm_mode = True

class Comment(BaseModel):
    comment:str

class User(BaseModel):
    username:str
    password : str
    description:Optional[str]
    phone:str
    email:EmailStr
    name:str
    public:Optional[bool] = True

class User_update(BaseModel):
    password : str
    description:Optional[str]
    phone:str
    email:EmailStr
    name:str
    public:Optional[bool]

class Userlogin(BaseModel):
    username:str
    password:str
    



class comment(BaseModel):
    comment:str

class token_id(BaseModel):
    token:str

class token(BaseModel):
    access_token :str
    token_type :str
    class Config:
        orm_mode = True

class tokendata(BaseModel):
    id:str          

