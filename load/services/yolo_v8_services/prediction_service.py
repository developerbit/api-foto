from utils.send_errors import send_errors    
from fastapi.encoders import jsonable_encoder

class PredictionService:

    @staticmethod
    def predict(image, model):
        try:
            results = model(image)
            print("Resultados brutos del modelo:", results)  
            predictions = []
            for result in results:
                for box in result.boxes:
                    prediction = {
                            "class_id": int(box.cls),
                            "class_name": result.names[int(box.cls)],
                            # "confidence": float(box.conf),
                            "bbox": box.xyxy.tolist()
                            }
                    predictions.append(prediction)
            # return jsonable_encoder(results)
            return predictions

            if not results:
                raise ValueError("No se encontraron resultados en la imagen.")
            return results
        except Exception as e:

            return send_errors(str(e), 500, 'prediction_service', 13)
