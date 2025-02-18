import os
from fastapi.encoders import jsonable_encoder
from ultralytics import YOLO
from utils.send_errors import send_errors    
from load.services.env_service import get_enviroment 

class ModelService:


    def load_model(self, id_modelo, enterprise):
        folder = get_enviroment('FOLDER_MODEL')
        path = f"{folder}{enterprise}/{id_modelo}.pt" 
        try:
            path = f"{folder}{enterprise}/{id_modelo}.pt" 
            model = YOLO(path)
            return model
        except KeyError as e:
            return send_errors(f"Error al cargar modelos, model_path: {path}, asegurate que el modelo existe.", 500, 'load_model', 13)
