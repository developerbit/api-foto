from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List
import httpx

# Pydantic models
class ConteoClaseBase(BaseModel):
    clase: str
    cantidad: int


class DetallePrediccionBase(BaseModel):
    id_image:int
    clase: str
    x_min: float
    y_min: float
    x_max: float
    y_max: float   