import os
from dotenv import load_dotenv
load_dotenv()
from load.model.util import Util
from fastapi.responses import JSONResponse
from fastapi import Request
import numpy as np
import pandas as pd 
import torch
import cv2
from super_gradients.training import models
from load.model.get_etiquetas import get_classes
from load.model.get_modelos import get_modelo


class ModeloYoloNas:
    
    #En esta funcion llega el json con la peticion 
    async def AnalyzeModel(self,request: Request):
        global model, device
        
        # Obtener las clases desde la API
        data = await request.json()
        classes = get_classes(data['id_modelo'])
        #test=get_modelo(1)
        #test=get_modelo(data['id_modelo'])

        
         #Obtener el nombre del modelo via API y devuelve el path del modelo
        model_path = os.environ.get(get_modelo(data['id_modelo']))
        #print(model_path)

        model = models.get(
            'yolo_nas_m',
            pretrained_weights="coco",
            num_classes=len(classes),
            checkpoint_path=model_path
        )
 
        # Ahora mueve el modelo al dispositivo apropiado.
        device = "mps" if torch.backends.mps.is_available() else "cpu"
        model = model.to(device)
        
        #Ruta para guardar la imagen 
        file_name = Util.Download(os.environ.get('UPLOAD_FOLDER_POSTOBON'), data['url_image'])
        
        #Carga la imagen en un formato especifico
        image = cargar_imagen(file_name)
        #print(image)    
            
        prediction = prediccion(image)
   
            
            # Mostrar conteo de clases detectadas
        class_counts = mostrar_clases(prediction.prediction.labels, classes)
        df_counts = pd.DataFrame(list(class_counts.items()), columns=['Producto', 'Cantidad'])

            
            # Mostrar detalle de la predicción
        df_prediccion = formatear_prediccion(prediction, classes)

        resultados = {
          "conteo_clases": df_counts.to_dict(orient="records"),
          "detalle_prediccion": df_prediccion.to_dict(orient="records")
          }

            # Convertir el diccionario a JSON y devolverlo como respuesta
        return JSONResponse(content=resultados)
            
            
def prediccion(image):
                    
                    # Asegurar que la imagen esté en el formato y dispositivo correcto
                    image_tensor = torch.from_numpy(image).to(device).float()
                    
                    image_tensor = image_tensor.permute(2, 0, 1).unsqueeze(0)  # De HWC a CHW y agregar dimensión de batch
                    outputs = model.predict(image_tensor)
                    return outputs

def formatear_prediccion(outputs, class_names):
                        bboxes = outputs.prediction.bboxes_xyxy
                        labels = outputs.prediction.labels
                        # Asumimos que no hay puntuaciones de confianza disponibles.
            
                        data = [{
                            'Producto': class_names[label],
                            'x_min': round(bbox[0], 2),
                            'y_min': round(bbox[1], 2),
                            'x_max': round(bbox[2], 2),
                            'y_max': round(bbox[3], 2)
                        } for label, bbox in zip(labels, bboxes)]
                
                        return pd.DataFrame(data)
            
def mostrar_clases(labels, class_names):
                        from collections import Counter
                        # Contar las ocurrencias de cada etiqueta de clase en las etiquetas detectadas
                        counts = Counter(labels)
                        # Mapear índices a nombres de clases y devolver un diccionario
                        class_counts = {class_names[label]: count for label, count in counts.items()}
                        return class_counts
            
#Este codigo recibe la imagen
def cargar_imagen(image_file):
    
    img = cv2.imread(image_file)
    if img is None:
        raise ValueError("No se pudo cargar la imagen desde la ruta especificada:", image_file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img
            
