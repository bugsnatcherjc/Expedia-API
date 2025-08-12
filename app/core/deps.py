from app.services.home_service import HomeService

def get_home_service() -> HomeService:
    return HomeService()