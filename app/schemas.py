from datetime import datetime
from pydantic import BaseModel, EmailStr, constr


class UserBaseSchema(BaseModel):
    firstname: str
    lastname: str
    phone: str
    wantnotification: bool
    wanthistory: bool
    level: int
    co2saved: int
    email: EmailStr
    photo: str
    role: str 
    created_at: datetime
    updated_at: datetime 

    class Config:
        orm_mode = True

class UserUpdateSchema(BaseModel):
    firstname: str
    lastname: str
    phone: str
    wantnotification: bool
    wanthistory: bool
    level: int
    co2saved: int
    email: EmailStr
    photo: str
    role: str 


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    passwordConfirm: str
    verified: bool = False


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserResponseSchema(UserBaseSchema):
    id: str
    pass


class UserResponse(BaseModel):
    status: str
    user: UserResponseSchema
