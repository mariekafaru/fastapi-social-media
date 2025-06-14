from fastapi import FastAPI, APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from src.social_media.database import get_db
from src.social_media import schemas, models, utils,oauth2 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router=APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login( user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    #create access_token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}




