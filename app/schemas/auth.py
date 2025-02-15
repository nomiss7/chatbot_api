from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserVerify(BaseModel):
    email: str
    verification_code: str


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    token: str
