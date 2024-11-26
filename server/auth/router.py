from typing import Optional, Annotated

from fastapi import HTTPException, APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from auth.schemes import Token, UserParams
from auth.utils import create_jwt, decode_jwt, get_user, add_user_in_db
from database import get_db
from models import User

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

router_token = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register(user_params: UserParams, db: Session = Depends(get_db)):
    user = get_user(user_params.username, db)
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(user_params.password)
    user = User(username=user_params.username, email=user_params.email, password=hashed_password)
    add_user_in_db(user, db)
    return {"msg": "User registered successfully"}

@router_token.post('/token')
async def post_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    db_user = get_user(form_data.username, db)
    if not db_user or not pwd_context.verify(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_jwt(data={"sub": form_data.username, 'jti': str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(access_token: Optional[str] = Depends(oauth2_scheme),  db: Session = Depends(get_db)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = decode_jwt(token=access_token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid token")
    return get_user(username, db)

@router.get("/me")
async def me(user: UserParams = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return {"username": user.username}