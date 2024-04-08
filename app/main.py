from fastapi import FastAPI
from .routers import users,auth,posts
import uvicorn


app = FastAPI()
app.include_router(users.router)  #routing 
app.include_router(posts.router)  #routing 
app.include_router(auth.router)  #routing 

@app.get("/")
def root():
    return {"data":"hello world"}


# if __name__ == "__main__":
#     uvicorn.run(app=app,host="0.0.0.0",reload=True) uvicorn app.main:app --reload