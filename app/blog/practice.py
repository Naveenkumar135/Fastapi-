from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


app=FastAPI()
# @app.get('/blog/100')
# def index():
#     return {'name':100}

@app.get('/blog/{id}')
def show(id):
    return {'name':id}

# @app.get('/blog/{id}/comments')
# def show(id):
#     return {'name':id,'data':{1,3}}

@app.get('/blog/{id}/comments')
def number(id: int):
    return {'name':id,'data':{1,3}}

# @app.get('/blog')
# def index(limit,published):
#     if published:
#         return {'data':f'{limit} blogs are published from db'}
#     else:
#         return {'data':f'{limit} blogs are from db'}


#for this path should be localhost:8000/blog?limit=10&published=true

# @app.get('/blog')
# def index(limit=10,published:bool=True):
#     if published:
#         return published
#     else:
#         return not published

@app.get('/blog')
def index(limit,published:bool):
    if published:
        return {'data':f'{limit} blogs are published from db'}
    else:
       return {'data':f'{limit} blogs are from db'}
    
class Blog(BaseModel):
    title:str
    body:str


@app.post('/blog')
def index(request:Blog):
    return {'data':f'created a blog with title {request.title}'}











from fastapi import FastAPI,Depends,status,Response,HTTPException


from . import schemas,models,hashing

from database import engine,SessionLocal

from sqlalchemy.orm import Session

from typing import List

models.Base.metadata.create_all(engine)

def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close()


app=FastAPI()
# @app.post('/blog')
# def index(request:schemas.Blog):
#     return {'data':f'created a blog with title {request.title}'}

## create a blog

# @app.post('/blog')
# def create(request:schemas.Blog,db:Session=Depends(get_db)):
#     new_blog=models.Blog(title=request.title,body=request.body)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog




## get a blog
@app.get('/blog',response_model=List[schemas.ShowBlog],tags=["blogs"])
def all(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs


# @app.get('/blog/{id}')
# def show(id:int ,db:Session=Depends(get_db)):
#     blogs=db.query(models.Blog).filter(models.Blog.id==id).first()
#     return blogs

@app.post('/blog',status_code=status.HTTP_201_CREATED,tags=["blogs"])
def create(request:schemas.Blog,db:Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=["blogs"])
def destroy(id:int,db:Session=Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return 'done'

# @app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
# def update(id:int,request:schemas.Blog,db:Session=Depends(get_db)):
#     db.query(models.Blog).filter(models.Blog.id==id).update({"title":'updated title'})
#     db.commit()
#     return 'updated'


# @app.post('/blog',status_code=status.HTTP_201_CREATED)
# def create(request:schemas.Blog,db:Session=Depends(get_db)):
#     new_blog=models.Blog(title=request.title,body=request.body)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog





@app.get('/blog/{id}',status_code=200,response_model=schemas.ShowBlog,tags=["blogs"])
def show(id:int ,response:Response,db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f'Blog with id {id} is not available '}
    return blogs


@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=["blogs"])
def update(id:int,request:schemas.Blog,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
    blog.update(request)
    db.commit()
    return 'updated'


@app.post('/user',tags=["user"])
def create(request:schemas.User,db:Session=Depends(get_db)):
    new_user=models.User(name=request.name,email=request.email,password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user



@app.get('/user/{id}',status_code=200,response_model=schemas.ShowUser,tags=["user"])
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.user_id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} not found')
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f'Blog with id {id} is not available '}
    return user

