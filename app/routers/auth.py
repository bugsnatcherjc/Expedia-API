from fastapi import APIRouter, Depends
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/")
async def get_auth(service: AuthService = Depends()):
    return service.get_auth()