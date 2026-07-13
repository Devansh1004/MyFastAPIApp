from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class PostSchema(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    
my_posts = []

@app.get("/")
async def root():
    return {"message": "Hello World, This is an API"}

@app.get("/posts")
def get_posts():
    return {"num": 2, "posts": {"content1":"Hey Mom"}}
    
@app.post("/posts")
def create_post(post: PostSchema):
    print(post)
    print(post.model_dump())    
    return {"message": "Successfully created post"}