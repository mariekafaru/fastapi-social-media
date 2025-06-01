from pydantic import BaseModel, EmailStr, Field
from datetime import datetime 
from typing import Optional
from typing import Annotated

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True  

class UserLogin(BaseModel):
    email: EmailStr  
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut

    class Config:
        orm_mode = True
        
class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    email: EmailStr

    class Config:
        orm_mode = True


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]  

