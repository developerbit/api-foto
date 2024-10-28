from utils.send_errors import send_errors    

class PredictionService:
    
    @staticmethod
    def predict(image, model):
        try:
            results = model(image)
            if not results:
                raise ValueError("No se encontraron resultados en la imagen.")
            return results
        except Exception as e:
            return send_errors(str(e), 500, 'prediction_service', 13)
