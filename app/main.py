from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users,auth,posts
import uvicorn


app = FastAPI()
app.include_router(users.router)  #routing 
app.include_router(posts.router)  #routing 
app.include_router(auth.router)  #routing 

@app.get("/")
def root():
    return {"data":"hello world"}
app.add_middleware(
    CORSMiddleware,
    allow_origins  =["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# if __name__ == "__main__":
#     uvicorn.run(app=app,host="0.0.0.0",reload=True) uvicorn app.main:app --reload