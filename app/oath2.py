from jose import JWTError,jwt   
from datetime import datetime,timedelta
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from . import schema

secret_key = "5as5d65adad65a4ds683awd9awd5a8wdd45ad5a34dawdad533ad4ef6dvdr6gd"
Algorithm  = "HS256"
Expiration_time = 30

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")  # for request to "/login"  tokenUrl = "login"

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp":expire})
    token  = jwt.encode(to_encode,secret_key,algorithm=Algorithm)

    return token


def verify_access_token(token:str,credential_exception):  #token is taken input in this function from postman
  try: 
   payload = jwt.decode(token,secret_key,algorithms=[Algorithm])
   id:str = payload.get("user_id")
   if not id:
       raise credential_exception
   token_data = schema.tokendata(id=id)
  except JWTError:
    raise credential_exception
  return token_data   


def get_current_user(token:str=Depends(oauth2_schema)):
   credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid credential")

   return   verify_access_token(token,credential_exception)