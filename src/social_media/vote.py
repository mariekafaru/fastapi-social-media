from fastapi import APIRouter, Depends, HTTPException, status
from src.social_media import models, schemas, oauth2
from src.social_media.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix='/votes', tags=['votes'])

@router.post('/', status_code=201)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {vote.post_id} does not exist')
    vote_query=db.query(models.Vote).filter(
            models.Vote.post_id == vote.post_id,
            models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if (vote.dir ==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User has already voted on this post')
        new_vote=models.Vote(post_id= vote.post_id, user_id= current_user.id)
        db.add(new_vote)
        db.commit()
        return new_vote
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vote does not exist')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message': 'Vote deleted successfully'}