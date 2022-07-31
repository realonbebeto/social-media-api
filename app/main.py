from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import *
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{'title': "hello, I am here", 'content': "Well, its my first time", "id": 1}, {
    "title": "favourite foods", 'content': "pizza, tripe, succotache", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello, Bebeto"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict, "my_posts": my_posts}


@app.get("/posts/latest")
async def get_post_latest():
    post = my_posts[len(my_posts)-1]
    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"Post with id '{id}' not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post found")
    return {"post_detail": post}

# Paths with {} placeholders should come last when they have matching methods


@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    post = find_post(id)

    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"Post with id '{id}' not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id '{id}' not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    idx = find_index_post(id)
    if idx == None:
        #response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"Post with id '{id}' not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id '{id}' not found")
    my_posts.pop(idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def update_post(id: int, post: Post):
    idx = find_index_post(id)

    if idx == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[idx] = post_dict
    return {"data": my_posts}
