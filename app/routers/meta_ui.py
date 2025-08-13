from fastapi import APIRouter
from app.services import meta_ui_service

router = APIRouter(prefix="/meta-ui", tags=["Meta / Dropdown Data"])

@router.get("/stays/locations")
async def stays_locations():
    return meta_ui_service.get_stays_locations()

@router.get("/stays/amenities")
async def stays_amenities():
    return meta_ui_service.get_stays_amenities()

@router.get("/stays/stars")
async def stays_stars():
    return meta_ui_service.get_stays_stars()

@router.get("/airports")
async def airports():
    return meta_ui_service.get_airports()

@router.get("/airlines")
async def airlines():
    return meta_ui_service.get_airlines()

@router.get("/cars/locations")
async def car_locations():
    return meta_ui_service.get_car_locations()

@router.get("/cars/brands")
async def car_brands():
    return meta_ui_service.get_car_brands()

@router.get("/currencies")
async def currencies():
    return meta_ui_service.get_currencies()

@router.get("/languages")
async def languages():
    return meta_ui_service.get_languages()
