from fastapi import FastAPI
from app.routes.validation import router as validation_router

app = FastAPI(title="Photo Validation Service")

app.include_router(validation_router, prefix="/validate")