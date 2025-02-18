from load.services.yolo_v8_services.prediction_service import PredictionService
from load.services.yolo_v8_services.result_service import ResultService

class ModuleService:
    def __init__(self):
        self.model_service = ModelService()
        self.image_service = ImageService()

    def competitionModule (self ,image, formatted_json):
            model = self.model_service.load_model(0)
            results = PredictionService.predict(image, model)
            total = ResultService.total_result(results)
            formatted_json['total'] = total
            return formatted_json
