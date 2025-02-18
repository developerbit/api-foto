import pandas as pd 
import torch
from  utils.send_errors import send_errors    

class PredictionService:

    def prediccion(image, model, device):
        try:                  
            # Asegurar que la imagen esté en el formato y dispositivo correcto
            image_tensor = torch.from_numpy(image).to(device).float()
            
            image_tensor = image_tensor.permute(2, 0, 1).unsqueeze(0)  # De HWC a CHW y agregar dimensión de batch
            outputs = model.predict(image_tensor)
            return outputs
        except KeyError as e:
            return send_errors(str(e),500, 'prediction_service', 18)

    def mostrar_clases(labels, class_names):
        try:
            from collections import Counter
            # Contar las ocurrencias de cada etiqueta de clase en las etiquetas detectadas
            counts = Counter(labels)
            # Mapear índices a nombres de clases y devolver un diccionario
            class_counts = {class_names[label]: count for label, count in counts.items()}
            return class_counts
        except KeyError as e:
            return send_errors(str(e),500, 'prediction_service', 18)


    def formatear_prediccion(outputs, class_names):
        try:
            bboxes = outputs.prediction.bboxes_xyxy
            labels = outputs.prediction.labels

            data = [{

                'classname': class_names[label],
                'xMin': round(bbox[0], 2),
                'yMin': round(bbox[1], 2),
                'xMax': round(bbox[2], 2),
                'yMax': round(bbox[3], 2)
            } for label, bbox in zip(labels, bboxes)]

            return pd.DataFrame(data)
        except KeyError as e:
            return send_errors(str(e),500, 'prediction_service', 18)


    def total_image(outputs):
        try:
            return outputs
        except KeyError as e:
            return send_errors(str(e),500, 'prediction_service', 18)
