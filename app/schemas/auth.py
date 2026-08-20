from pydantic import BaseModel

class Auth():

    class UserBase(BaseModel):
        email: str
        username: str

    class SignupRequest(UserBase):
        password: str
        department_id:int

    class LoginRequest(BaseModel):
        email: str
        password: str
        department_id : int | None = None

    class TokenResponse(BaseModel):
        access_token: str
        token_type: str = "bearer"

    class RefreshToken(TokenResponse):
        refresh_token: str

    class AuthResponse(BaseModel):
        message: str
        user: RefreshToken



