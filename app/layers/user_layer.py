from fastapi import HTTPException,status
from .. import schema
from datetime import datetime
from ..database import conn,cursor

def create_user(user:schema.User):
    cursor.execute(""" select count(*) as cnt from test_user where username = %s""",(user.username,))
    existing_user = cursor.fetchone()
    print(type(existing_user["cnt"]))
    if int(existing_user["cnt"]) > 0 :

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="username already exists")
    
    cursor.execute(""" insert into test_user (username,password,description,phone,email,name,public) values (%s,%s,%s,%s,%s,%s,%s) returning * """,(user.username,user.password,user.description,user.phone,user.email,user.name,user.public,))
    new_user = cursor.fetchone()

    conn.commit()
    return {"username":new_user["username"],"created_at":((datetime.now())),"description":new_user["description"],"user_id":new_user["user_id"],"name":new_user["name"]}


def change_user(user:schema.User_update,id):
    if user.public is None:
        cursor.execute(""" update test_user set password = %s,description = %s,phone = %s,email = %s,name = %s where user_id = %s""",(user.password,user.description,user.phone,user.email,user.name,id,))
    else:
        cursor.execute(""" update test_user set password = %s,description = %s,phone = %s,email = %s,name = %s,public = %s where user_id = %s""",(user.password,user.description,user.phone,user.email,user.name,user.public,id,))
    conn.commit()
    return {"detail":"user_updated"}


def get_user(id:int):
    cursor.execute(""" select count(*) as cnt from test_user where user_id =%s """,(id,))
    existing_user = cursor.fetchone()
    if existing_user["cnt"]==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user does not exists")
    
    cursor.execute(""" select username,Name,user_id,case when description is null then name else description end as description from test_user where user_id = %s """,(id,))
    user = cursor.fetchone()
    return user

def get_users():
    cursor.execute(""" select username,user_id,Name,case when description is null then name else description end as description from test_user """)
    user = cursor.fetchall()
    return user


def user_login(username:str):
    cursor.execute(""" select username,password,user_id from test_user where username = %s""",(username,))
    user = cursor.fetchone()
    return user


def send_request(id1:int,id2:int):
    cursor.execute(""" select count(*) as cnt from test_req where (user_send = %s and user_recv = %s) or (user_send = %s and user_recv = %s)""",(id1,id2,id2,id1,))
    existing_req = cursor.fetchone()
    if existing_req["cnt"]>0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="request already sent")

    cursor.execute(""" select count(*) as cnt from test_user where user_id =%s """,(id1,))
    existing_user = cursor.fetchone()
    if existing_user["cnt"]==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user does not exists")

    cursor.execute("""insert into test_req (user_recv,user_send,status) values (%s,%s,%s)""",(id1,id2,str(0),))
    conn.commit()
    return{"detail":"request sent"}


def accept_request(id1:int,id2:int):
    cursor.execute(""" select count(*) as cnt from test_req where status = True and ((user_send = %s and user_recv = %s) or (user_send = %s and user_recv = %s))""",(id1,id2,id2,id1,))
    existing_req = cursor.fetchone()
    if existing_req["cnt"]>0:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="request already accepted")
    
    cursor.execute(""" select count(*) as cnt from test_req where user_send = %s and user_recv = %s """,(id1,id2,))
    existing_req = cursor.fetchone()
    if existing_req["cnt"]>0:
         cursor.execute(""" update test_req set status = True where user_send = %s and user_recv = %s  """,(id1,id2,))
         conn.commit()

    else:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="request not present")    
    
    return{"detail":"request accepted"}


def reject_request(id1:int,id2:int):
    cursor.execute(""" select count(*) as cnt from test_req where user_send = %s and user_recv = %s """,(id1,id2,))
    existing_req = cursor.fetchone()
    if existing_req["cnt"]>0:
         cursor.execute(""" delete from test_req where user_send = %s and user_recv = %s  """,(id1,id2,))
         conn.commit()

    else:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="request not present")    
    
    return{"detail":"request rejected"}

