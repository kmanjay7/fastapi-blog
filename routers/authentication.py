from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..config import database, token
from ..schema import schemas
from ..models import models
from ..config.hashing import Hash
from sqlalchemy.orm import Session
router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}