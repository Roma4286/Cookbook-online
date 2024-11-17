from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class UserParams(BaseModel):
    username: str
    email: str
    password: str
