from ..layers.user_layer import create_user,get_user,get_users,send_request,accept_request,reject_request
from fastapi import status,HTTPException,APIRouter,Depends
from typing import List
from .. import schema,util,oath2

router = APIRouter(
    tags=["users"]
) 


@router.post("/createuser", status_code=status.HTTP_201_CREATED, response_model=schema.User_Response)
def Create_user(user:schema.User):
    user.password = util.hash(user.password)  #hashing the password
    new_user = create_user(user)
    return new_user


@router.get("/users/{id}",response_model=schema.User_Response)
def get_User(id:int,get_current_user = Depends(oath2.get_current_user)):
    user = get_user(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user not found")
    return user


@router.get("/users",response_model=List[schema.User_Response])
def get_Users(get_current_user = Depends(oath2.get_current_user)):
    users = get_users()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="NO users found")
   
    return users




#sending and accepting requests
@router.post("/request/{id}")
def request1(id:int,get_current_user = Depends(oath2.get_current_user)):
    payload = send_request(id,get_current_user.id)
    return payload

@router.put("/accept/{id}")
def request2(id:int,get_current_user = Depends(oath2.get_current_user)):
    payload = accept_request(id,get_current_user.id)
    return payload

@router.delete("/reject/{id}")
def request3(id:int,get_current_user = Depends(oath2.get_current_user)):
    payload = reject_request(id,get_current_user.id)
    return payload
