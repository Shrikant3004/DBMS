from fastapi import HTTPException,status
from .. import schema
from datetime import datetime
from ..database import conn,cursor

def insert_post(post:schema.POST_Create,user_id):
    cursor.execute(""" insert into test_post(title,content,description,user_id) values(%s,%s,%s,%s) returning *""",(post.title,post.content,post.description,user_id,))
    response = cursor.fetchone()
    conn.commit()
    cursor.execute("""select username from test_user where user_id = %s""",(response["user_id"],))
    user = cursor.fetchone()


    return {"title":response["title"],"content":response["content"],"description":response["description"],"post_id":response["post_id"],"created_at":(datetime.now()),"username":user["username"],"user_id":response["user_id"]}


def change_post(id:int,post:schema.POST_Create,user_id):
    cursor.execute("""select count(*) as cnt from test_post where user_id = %s and post_id = %s""",(user_id,id,))
    existing_posts = cursor.fetchone()
    if existing_posts["cnt"] <= 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")
    
    cursor.execute(""" update test_post set title = %s, content = %s, description = %s where post_id = %s  returning *""",(post.title,post.content,post.description,id,))
    response = cursor.fetchone()
    conn.commit()
    cursor.execute("""select username from test_user where user_id = %s""",(response["user_id"],))
    user = cursor.fetchone()


    return {"title":post.title,"content":post.content,"description":post.description,"post_id":response["post_id"],"created_at":(datetime.now()),"username":user["username"],"user_id":response["user_id"]}


def remove_post(id:int,user_id):
    cursor.execute("""select count(*) as cnt from test_post where user_id = %s and post_id = %s""",(user_id,id,))
    post = cursor.fetchone()
    if post["cnt"] <= 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")
    
    cursor.execute(""" delete from test_post where post_id = %s""",(id,))
    conn.commit()
    return {"detail":f"post-{id} deleted"}


def retrieve_posts(id:int):
    cursor.execute("""select p.title,p.content,p.description,p.created_at,u.username,p.post_id,p.user_id from test_post p join test_user u on p.user_id = u.user_id where p.user_id =any( select users_friend from user_view where user_id = %s)""",(id,))
    available_post = cursor.fetchall()
    return available_post

def retrieve_post(user_id:int,id:int):
    #id = friend's id
    cursor.execute(""" select count(*) as cnt from test_user where user_id =%s """,(id,))
    existing_user = cursor.fetchone()
    if existing_user["cnt"]==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user does not exists")

    cursor.execute(""" select count(*) as cnt from user_view where user_id = %s and users_friend = %s""",(user_id,id,) )
    friend = cursor.fetchone()
    if friend["cnt"] <=0 :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="send request to see the post")
    
    cursor.execute("""select count(*) as cnt from test_post where user_id =any( select users_friend from user_view where user_id = %s and users_friend = %s)""",(user_id,id,))
    post = cursor.fetchone()
    if post["cnt"] <=0 :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user has no posts")
    
    cursor.execute("""select p.title,p.content,p.description,p.created_at,u.username,p.post_id,p.user_id from test_post p join test_user u on p.user_id = u.user_id where p.user_id =any( select users_friend from user_view where user_id = %s and users_friend = %s)""",(user_id,id))
    available_post = cursor.fetchall()
    return available_post

def like_post(post_id,user_id):
    cursor.execute("""select count(*) as cnt from user_view where users_friend = (select user_id from test_post where post_id = %s) and user_id = %s """,(post_id,user_id,))
    existing_post = cursor.fetchone()
    if (existing_post["cnt"] <= 0):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid like")
    
    cursor.execute("""select count(*) as cnt from test_like where post_id = %s and user_id = %s """,(post_id,user_id,))
    existing_like = cursor.fetchone()
    if(existing_like["cnt"]>0):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="already liked")

    cursor.execute("""insert into test_like (user_id,post_id) values(%s,%s) returning * """,(user_id,post_id,))
    conn.commit()
    return {"detail":f"user {user_id} liked post {post_id}"}

def remove_like(post_id,user_id):
     cursor.execute("""select count(*) as cnt from test_like where post_id = %s and user_id = %s """,(post_id,user_id,))
     existing_like = cursor.fetchone()
     if(existing_like["cnt"]>0):
        cursor.execute("""delete from test_like where post_id = %s and user_id = %s """,(post_id,user_id,))
        conn.commit()
        return {"detail":f"like removed from user {user_id} on post {post_id}"}
     else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post is not liked")
     

def add_comment(post_id,user_id,comment):
    cursor.execute("""select count(*) as cnt from user_view where users_friend = (select user_id from test_post where post_id = %s) and user_id = %s """,(post_id,user_id,))
    existing_post = cursor.fetchone()
    if (existing_post["cnt"] <= 0):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid comment")
    
    cursor.execute("""insert into test_comment (post_id,user_id,comment) values (%s,%s,%s) returning * """,(post_id,user_id,comment,))
    comment_id = cursor.fetchone()["comment_id"]
    conn.commit()
    return {"user_id":user_id,"post_id":post_id,"comment":comment,"comment_id":comment_id}

def remove_comment(comment_id,user_id):
    cursor.execute("""select count(*) as cnt from test_comment where comment_id = %s and user_id = %s""",(comment_id,user_id,))
    existing_comment = cursor.fetchone()
    if(existing_comment["cnt"]>0):
        cursor.execute("""delete from test_comment where comment_id = %s """,(comment_id,))
        conn.commit()
        return {"detail":f"comment removed"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="comment is not present for this user")
    

def get_comms(post_id):
    cursor.execute("""select * from test_comment where post_id = %s""",(post_id,))
    response = cursor.fetchall()
    return response    