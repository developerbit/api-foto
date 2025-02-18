from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Request
from load.services.yolo_v8_services.image_service import ImageService
from load.services.yolo_v8_services.model_service import ModelService
from load.services.yolo_v8_services.prediction_service import PredictionService
from load.services.yolo_v8_services.result_service import ResultService
from load.services.yolo_v8_services.module_service import ModuleService

class ModeloYoloV8:
    
    def __init__(self):
        self.model_service = ModelService()
        self.image_service = ImageService()

    async def AnalyzeModel(self, request: Request, model, enterprise):
        try:
            data = await request.json()
            # return data
            modulo = data['modulo']
            model = self.model_service.load_model(model, enterprise)

            file_name = self.image_service.process_image(data['url_image'])
            image = self.image_service.load_image(file_name)

            results = PredictionService.predict(image, model)
            # return jsonable_encoder(results)

            if not results:
                return JSONResponse(content={"error": "No se encontraron resultados en la imagen."}, status_code=500)

            formatted_json = ResultService.format_results(results, model, data)
            # print(formatted_json)
            if modulo == 47:
                ModuleService.competitionModule(self, image,formatted_json)

            return formatted_json

            # return JSONResponse(content=formatted_json, status_code=200)

        except Exception as e:
            return JSONResponse(content={"error": f"Error en el proceso de inferencia: {str(e)}"}, status_code=500)

