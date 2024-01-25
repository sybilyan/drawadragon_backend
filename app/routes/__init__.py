from fastapi import FastAPI, APIRouter
from app.routes.dragon import dragon_router

app = FastAPI()
api_router = APIRouter()


@api_router.get("/health_check")
def health_check():
    return "ok"


api_router.include_router(dragon_router)
