from passlib.context import CryptContext

current_context = CryptContext(schemes=["bcrypt"])

def hash(password:str):  #hashing of password 
    return current_context.hash(password)

def verify(password,hash_password):   #verifying password while login
   return current_context.verify(password,hash_password)
