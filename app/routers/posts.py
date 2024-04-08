from ..layers.post_layer import insert_post,change_post,remove_post,retrieve_posts,retrieve_post
from fastapi import status,HTTPException,APIRouter,Depends
from typing import List
from .. import schema,util,oath2

router = APIRouter(
    tags=["posts"]
) 

@router.post("/createpost",status_code=status.HTTP_201_CREATED,response_model=schema.POST_Response)
def create_post(post:schema.POST_Create,get_current_user = Depends(oath2.get_current_user)):
    response = insert_post(post,get_current_user.id)
    return response

@router.put("/updatepost/{id}",status_code=status.HTTP_200_OK,response_model=schema.POST_Response)
def update_post(id:int,post:schema.POST_Update,get_current_user = Depends(oath2.get_current_user)):
    response = change_post(id,post,get_current_user.id)
    return response

@router.delete("/deletepost/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,get_current_user = Depends(oath2.get_current_user)):
    response = remove_post(id,get_current_user.id)
    return response

@router.get("/posts",status_code=status.HTTP_200_OK,response_model=List[schema.POST_Response])
def get_posts(get_current_user = Depends(oath2.get_current_user)):
    posts = retrieve_posts(get_current_user.id)
    return posts

@router.get("/posts/{id}",status_code=status.HTTP_200_OK,response_model=List[schema.POST_Response])
def get_post(id:int,get_current_user = Depends(oath2.get_current_user)):
    post = retrieve_post(get_current_user.id,id)
    return post