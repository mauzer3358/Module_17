from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import *
from sqlalchemy import insert, select, update, delete
from app.schemas import CreateTask, UpdateTask

from slugify import slugify

router = APIRouter(prefix='/task', tags=['task'])


########################
@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int):
    search_user = db.scalar(select(User).where(User.id == user_id))
    if search_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    db.execute(insert(Task).values(title = create_task.title,
                                   content = create_task.content,
                                   priorety = create_task.priority,
                                   user_id = search_user.id,
                                   slug = slugify(create_task.title)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

###########################

@router.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_task: UpdateTask ):
    up_task = db.scalar(select(Task).where(Task.id == task_id))
    if up_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )

    db.execute(update(Task).where(Task.id == task_id).values(title = update_task.title,
                                                             priorety = update_task.priority,
                                                             content = update_task.content))
    db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task update is successful'
    }


@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    all_tasks = db.scalars(select(Task).where()).all()
    if all_tasks is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Tasks not found'
        )
    return all_tasks



@router.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    get_task = db.scalar(select(Task).where(Task.id == task_id))
    if get_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found'
        )
    else: return get_task





@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    del_task = db.scalar(select(User).where(Task.id == task_id))
    if del_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found'
        )
    else:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Task delete is successful'
        }