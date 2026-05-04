from pydantic import BaseModel

class ValidationResponse(BaseModel):
    sharpness: float
    brightness: float
    approved: bool