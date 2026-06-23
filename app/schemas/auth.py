from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    email:EmailStr
    password:str

class LoginResponse(BaseModel):
    acess_token:str
    token_type:str


class GoogleLoginRequest(BaseModel):
    id_token:str

class RefreshRequest(BaseModel):
    refresh_token:str