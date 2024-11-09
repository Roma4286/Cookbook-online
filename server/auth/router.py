from fastapi import HTTPException, Response, Cookie, APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from passlib.context import CryptContext
from typing import Optional, Annotated
from pydantic import BaseModel
from server.auth.utils import create_jwt, decode_jwt

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

router_token = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {}

class User(BaseModel):
    username: str
    password: str

def get_user(username: str):
    return fake_users_db.get(username)

@router.post("/register")
async def register(user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    fake_users_db[user.username] = user
    return {"msg": "User registered successfully"}

class Token(BaseModel):
    access_token: str
    token_type: str


@router_token.post('/token')
async def post_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    db_user = get_user(form_data.username)
    if not db_user or not pwd_context.verify(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_jwt(data={"sub": form_data.username})

    return Token(access_token=access_token, token_type="bearer")

async def get_current_user(access_token: Optional[str] = Depends(oauth2_scheme)):
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
    return get_user(username)

@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return {"username": user.username}