from datetime import timedelta

JWT_SECRET = "jwt_secret"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    return "mock-token"

def verify_token(token: str) -> dict:
    if token == "mock-token":
        return {"sub": "user_mock"}
    raise Exception("Invalid token")