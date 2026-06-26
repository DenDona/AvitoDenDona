from app.ports.rest.api.v1.schema import BaseSchema


class RegisterRequest(BaseSchema):
    username: str
    password: str
    email: str | None = None


class UserResponse(BaseSchema):
    id: int
    username: str
    email: str | None


class LoginRequest(BaseSchema):
    login: str
    password: str


class TokenResponse(BaseSchema):
    access_token: str
    token_type: str = "bearer"
