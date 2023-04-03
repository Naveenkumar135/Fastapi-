from fastapi import APIRouter,Depends

from .. import schemas,database


from sqlalchemy.orm import Session

from ..repository import user

get_db=database.get_db

router=APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post('/')
def create(request:schemas.User,db:Session=Depends(get_db)):
    return user.create(request,db)



@router.get('/{id}',status_code=200,response_model=schemas.ShowUser)
def get_user(id:int,db:Session=Depends(get_db)):
    return user.get_user(id,db)