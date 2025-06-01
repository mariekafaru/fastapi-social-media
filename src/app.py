from fastapi import FastAPI
from src.social_media import models
from src.social_media.database import engine 
from .social_media.posts import post_router
from .social_media.users import user_router
from .social_media.auth import router as login_router
from .social_media.users import user_router
from .social_media.vote import router as vote_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(post_router)
app.include_router(user_router)
app.include_router(login_router)
app.include_router(vote_router)

