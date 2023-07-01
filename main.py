import uvicorn
from fastapi import FastAPI, Body, Depends
from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://tobiaswirtz:@postgres/postr"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


posts = [
    {
        "id": 1,
        "title": "apple",
        "text": "eat it"
    },
    {
        "id": 2,
        "title": "orange",
        "text": "eat it"
    },
    {
        "id": 3,
        "title": "peach",
        "text": "eat it"
    },
]

users = []

app = FastAPI()

@app.get("/", tags=["test"])
def greet():
    return {"Hello":"World!"}

@app.get("/posts", tags=["posts"])
def get_posts():
    return {"posts": posts}

@app.get("/post/{id}", tags=["posts"])
def get_post(id : int):
    for post in posts:
        if post["id"] == id:
            return {"post": post}


@app.post("/posts", dependencies=[Depends(jwtBearer())], tags=["posts"])
def add_post(post : PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "info": "Post added"
    }

@app.post("/user/signup", tags=["user"])
def user_signup(user: UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False
    
@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return {"error": "Invalid Login details"}