from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
import random
import time

app = FastAPI()

def generate_random_id(): 
    random.seed(int(time.time()))
    return random.randint(0,1000000000)
class PostSchema(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    id: int = Field(default_factory = generate_random_id)
    
    
my_posts = [
    PostSchema(title="Post 1", content="Content 1")
    ]

@app.get("/")
async def root():
    return {"message": "Hello World, This is an API"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}
    
@app.post("/posts")
def create_post(post: PostSchema):
    post_dict = post.model_dump()
    post_dict['id'] = generate_random_id()
    my_posts.append(post_dict)
    return {"data": post_dict, "length": len(my_posts)}