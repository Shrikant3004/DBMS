from ..layers.post_layer import insert_post,change_post,remove_post,retrieve_posts,retrieve_post,like_post,remove_like,add_comment,remove_comment,get_comms
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

@router.post("/like/{id}",status_code=status.HTTP_200_OK)
def like(id:int,get_current_user = Depends(oath2.get_current_user)):
    response = like_post(id,get_current_user.id)
    return response

@router.delete("/removelike/{id}",status_code=status.HTTP_204_NO_CONTENT)
def removelike(id:int,get_current_user = Depends(oath2.get_current_user)):
    response = remove_like(id,get_current_user.id)
    return response

@router.post("/comment/{id}",status_code=status.HTTP_201_CREATED) #id  = post_id
def comment(id:int,comment:schema.Comment,get_current_user = Depends(oath2.get_current_user)):
    response = add_comment(id,get_current_user.id,comment.comment)
    return response

@router.delete("/deletecomment/{id}",status_code=status.HTTP_204_NO_CONTENT) #id =comment_id
def delete_comment(id:int,get_current_user = Depends(oath2.get_current_user)):
    response = remove_comment(id,get_current_user.id)
    return response

@router.get("/getcomments/{id}",status_code=status.HTTP_200_OK) #id = post_id
def get_comments(id:int,get_current_user = Depends(oath2.get_current_user)):
    response = get_comms(id)
    return response