import time
import uuid
from datetime import datetime, timedelta

from jose import jwt
from sqlalchemy.orm import Session

from models import User
from config import settings

def add_user_in_db(user: User, db: Session):
    db.add(user)
    db.commit()

def get_user(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    return user

def create_jwt(
    data: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    now = datetime.fromtimestamp(time.time())
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded

