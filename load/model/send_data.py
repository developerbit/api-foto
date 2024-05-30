import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List
import httpx

# Modelo para contar las cantidades de las clases 
class ConteoClaseBase(BaseModel):
    clase: str
    cantidad: int

#Modelo con el detalle de la prediccion
class DetallePrediccionBase(BaseModel):
    id_image:int
    clase: str
    x_min: float
    y_min: float
    x_max: float
    y_max: float   

#Modelo con la data del Json
class RequestBody(BaseModel):
    conteo_clases: List[ConteoClaseBase]
    detalle_prediccion: List[DetallePrediccionBase]    



async def send_data_to_coordenadas(data: RequestBody):
    print(data)
    async with httpx.AsyncClient() as client:
        response = await client.post(os.environ.get("API_URL_POST_COORDENADAS"), json=data.dict())
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    return {"message": "Datos enviados correctamente"}


async def send_data_to_existing_api(data: RequestBody):
    print("send_data_to_existing_api llamada con datos:", data)
    data_dict = {
        #"conteo_clases": [item.dict() for item in data.conteo_clases],
        "detalle_prediccion": [item.dict() for item in data.detalle_prediccion]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(os.environ.get("API_URL_POST_COORDENADAS"), json=data_dict)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    print({"message": "Data sent successfully to the existing API"})
    return {"message": "Data sent successfully to the existing API"}