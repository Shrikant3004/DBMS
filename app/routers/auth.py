from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..layers.user_layer import user_login
from .. import database,util,schema,oath2
router = APIRouter(tags=["login"])

@router.post("/login")
def login(user_credential:OAuth2PasswordRequestForm=Depends()):
   user = user_login(user_credential.username)
   if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
   
   if not util.verify(user_credential.password,user["password"]):
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="wrong credential")
   
   access_token = oath2.create_access_token(data={"user_id":user["user_id"]})
   new_token = schema.token(access_token=access_token,token_type="bearer")
   return new_token