import os
from ultralytics import YOLO
from utils.send_errors import send_errors    

class ModelService:
    
    def __init__(self):
        self.model_paths = {
            3: os.getenv('YUPI'),
            4: os.getenv('AZULK'),
            5: os.getenv('RAMO'),
            9: os.getenv('KOALA')
            
        }
        self.models = {}

    def load_model(self, id_modelo):
        try:
            if id_modelo in self.models:
                return self.models[id_modelo]
            elif id_modelo in self.model_paths:
                model = YOLO(self.model_paths[id_modelo])
                self.models[id_modelo] = model
                return model
            else:
                raise ValueError(f"No se encontró un modelo para el id_modelo: {id_modelo}")
        except KeyError as e:
            return send_errors(f"Error al cargar modelos, model_path: {id_modelo}", 500, 'load_model', 13)
