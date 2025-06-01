from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, Response
from src.social_media.database import get_db
from src.social_media import models, schemas, oauth2
from typing import Optional
from sqlalchemy import func



post_router = APIRouter(prefix='/posts', tags=['posts'])

@post_router.get('/', response_model=list[schemas.PostOut])
def get_all_post(db: Session = Depends(get_db), current_user:int= Depends(oauth2.get_current_user), limit: int =3, skip: int = 0,search : Optional[str] = ""):
    results= db.query(models.Post, func.count(models.Vote.post_id)).join(models.Vote, models.Vote.post_id == models.Post.user.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results

@post_router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} not found')
    return result

@post_router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id= current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@post_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user:int= Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} not found')
    post = post.first()
    if post.user_id != oauth2.get_current_user().id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action')
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@post_router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user:int= Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} not found')
    if post.user_id != oauth2.get_current_user().id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
