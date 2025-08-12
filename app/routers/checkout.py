from fastapi import APIRouter, Depends
from app.services.checkout_service import CheckoutService

router = APIRouter(prefix="/checkout", tags=["Checkout"])

@router.get("/")
async def get_checkout(service: CheckoutService = Depends()):
    return service.get_checkout()
