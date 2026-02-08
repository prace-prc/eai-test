from fastapi import FastAPI
from app.api.order_api import router as order_router

app = FastAPI(title="Inspien EAI Service")

app.include_router(order_router)