from sqlalchemy.orm import session

from blog import models,schemas

from fastapi import status,HTTPException

def get_all(db:session):
    blogs=db.query(models.Blog).all()
    return blogs

def create(request: schemas.Blog,db:session):
    new_blog=models.Blog(title=request.title,body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def destroy(id,db:session):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return 'done'

def show(id,db:session):
    blogs=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f'Blog with id {id} is not available '}
    return blogs

def update(id,request:schemas.Blog,db:session):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
    blog.update(request)
    db.commit()
    return 'updated'

