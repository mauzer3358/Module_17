from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import *
from sqlalchemy import insert, select, update, delete
from app.schemas import CreateUser, UpdateUser

from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])

@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(insert(User).values(username = create_user.username,
                                   firstname = create_user.firstname,
                                   lastname = create_user.lastname,
                                   age = create_user.age,
                                   slug = slugify(create_user.username)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UpdateUser):
    up_user = db.scalar(select(User).where(User.id == user_id))
    if up_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )

    db.execute(update(User).where(User.id == user_id).values(firstname = update_user.firstname,
                                                             lastname = update_user.lastname,
                                                             age = update_user.age))
    db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful'
    }



@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    all_users = db.scalars(select(User).where()).all()
    if all_users is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Users not found'
        )
    return all_users





@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    get_user = db.scalar(select(User).where(User.id == user_id))
    if get_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    else: return get_user


@router.get("/user_id/tasks")
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    get_user_tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    if get_user_tasks is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Tasks not found'
        )
    return get_user_tasks, print(get_user_tasks)



@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    del_user = db.scalar(select(User).where(User.id == user_id))
    if del_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    else:
        db.execute(delete(User).where(User.id == user_id))
        db.execute(delete(Task).where(Task.user_id == user_id))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'User delete is successful'
        }