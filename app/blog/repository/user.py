from .. import schemas,models,hashing

from sqlalchemy.orm import session

from fastapi import status,HTTPException




def create(request:schemas.ShowUser,db:session):
    new_user=models.User(name=request.name,email=request.email,password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user

def get_user(id,db:session):
    user=db.query(models.User).filter(models.User.user_id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} not found')
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f'Blog with id {id} is not available '}
    return user