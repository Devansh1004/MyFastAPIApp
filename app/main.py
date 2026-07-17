from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
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

def find_post_by_id(id: int):
    for i,post in enumerate(my_posts):
        if post.id == id:
            return i,post
    return (None, None)

@app.get("/")
async def root():
    return {"message": "Hello World, This is an API"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}
    
@app.post("/posts")
def create_post(post: PostSchema):
    post.id = generate_random_id()
    my_posts.append(post)
    return {"data": post, "length": len(my_posts)}

@app.get("/posts/latest")
def get_latest():
    post = my_posts[-1]
    return {"message": post}

@app.get("/posts/{id}")
def get_post_by_id(id: int, response: Response):
    _,post = find_post_by_id(id)
    if post == None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : "post not found"}
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            "Post not found")
    else:
        return {"Post": post}
    
@app.delete("/posts/{id}")
def delete_post_by_id(id: int, response: Response):
    i,_ = find_post_by_id(id)
    if i == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    else:
        raise HTTPException(status.HTTP_204_NO_CONTENT)
    
    
@app.put("/posts/{id}")
def update_posts(id: int, post: PostSchema):
    index, old_post = find_post_by_id(id)
    if old_post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            "Post not found")
    my_posts[index] = post
    print(post)
    return {"message": "Updated post"}