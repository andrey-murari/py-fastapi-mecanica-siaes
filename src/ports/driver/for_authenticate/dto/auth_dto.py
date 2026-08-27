from pydantic import BaseModel, Field


class LoginDTO(BaseModel):
    login: str = Field(min_length=1)
    password: str = Field(min_length=1)


class TokenDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenClaimsDTO(BaseModel):
    sub: str
    user_type: str


class AdminIdentityDTO(BaseModel):
    login: str
    user_type: str
