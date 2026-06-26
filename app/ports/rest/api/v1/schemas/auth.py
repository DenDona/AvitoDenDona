from app.ports.rest.api.v1.schema import BaseSchema


class RegisterRequest(BaseSchema):
    username: str
    password: str
    email: str | None = None


class UserUpdateRequest(BaseSchema):
    phone: str | None = None
    avatar_url: str | None = None


class UserResponse(BaseSchema):
    id: int
    username: str
    email: str | None
    phone: str | None = None
    avatar_url: str | None = None


class LoginRequest(BaseSchema):
    login: str
    password: str


class TokenResponse(BaseSchema):
    access_token: str
    token_type: str = "bearer"