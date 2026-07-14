from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
from random import randint

app = FastAPI()

class PostSchema(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    id: int
    
my_posts = [{"title":"post 1", "content":"content 1", "id":1},
            {"title":"post 2", "content":"content 2", "id":2}]

@app.get("/")
async def root():
    return {"message": "Hello World, This is an API"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}
    
@app.post("/posts")
def create_post(post: PostSchema):
    post_dict = post.model_dump()
    post_dict['id'] = randint(0,100000000)
    my_posts.append(post_dict)
    return {"data": post_dict}