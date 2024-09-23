from fastapi.responses import JSONResponse
from  utils.send_errors import send_errors    
from fastapi import Request
from load.services.yolo_nas_services.model_service import load_model
from load.services.yolo_nas_services.image_service import cargar_image, process_image 
from load.services.yolo_nas_services.prediction_service import PredictionService
from load.services.yolo_nas_services.veredicto_service import VeredictoService

class ModeloYoloNas:
    
    async def AnalyzeModel(self,request: Request):
        try:
            global model, device

            data = await request.json()

            # extrayendo data del JSON
            id_modelo = data['id_modelo']
            url_image = data['url_image']
            etiquetas = data['etiquetas']
            imageUrl = data['url_image']
            imageId = data['id_image']
            telefono = data['telefono']

            #aqui se carga el modelo, se establece si usar cpu o mps, se establece el modelo y sus clases
            model, classes, device = load_model(id_modelo)

            #aqui se procesa la imagen y se formatea el nombre para evitar errores
            file_name = process_image(url_image)

            #aqui se carga la imagen para ser utilizada por el profeta
            image = cargar_image(file_name)

            # ok funciona
            # este es el profeta, y realiza las predicciones
            prediction = PredictionService.prediccion(image,model,device)
            # ok funciona

            # Mostrar detalle de la predicción
            df_prediccion = PredictionService.formatear_prediccion(prediction, classes)

            # Convertimos el DataFrame df_prediccion a una lista de diccionarios
            detalle_prediccion = df_prediccion.to_dict(orient="records")

            # Añadimos imageId a cada registro en detalle_prediccion
            veredictos, resultados = VeredictoService.jsonVeredict(detalle_prediccion,imageId,id_modelo,etiquetas,imageUrl,telefono)
            
            # En caso de que no llogue ningûn veredicto
            if len(veredictos) == 0:
                return JSONResponse({"imageId": imageId, "telefono": telefono, "url_image":imageUrl})
            
            return JSONResponse(resultados)
        except KeyError as e:
            return send_errors(str(e),500, 'yolo_nas', 18)

    #MODULO DE TEST Y AMBIENTE QA
    async def AnalyzeModel_test(self,request: Request):
        try:
            global model, device

            data = await request.json()

            # extrayendo data del JSON
            id_modelo = data['id_modelo']
            url_image = data['url_image']
            etiquetas = data['etiquetas']
            imageUrl = data['url_image']
            imageId = data['id_image']
            telefono = data['telefono']

            #aqui se carga el modelo, se establece si usar cpu o mps, se establece el modelo y sus clases
            model, classes, device = load_model(id_modelo)
            #aqui se procesa la imagen y se formatea el nombre para evitar errores
            file_name = process_image(url_image)

            #aqui se carga la imagen para ser utilizada por el profeta
            image = cargar_image(file_name)

            # este es el profeta, y realiza las predicciones
            prediction = PredictionService.prediccion(image,model,device)

            # Mostrar detalle de la predicción
            df_prediccion = PredictionService.formatear_prediccion(prediction, classes)

            # Convertimos el DataFrame df_prediccion a una lista de diccionarios
            detalle_prediccion = df_prediccion.to_dict(orient="records")

            # Añadimos imageId a cada registro en detalle_prediccion
            veredictos, resultados = VeredictoService.jsonVeredict(detalle_prediccion,imageId,id_modelo,etiquetas,imageUrl,telefono)
            
            # En caso de que no llogue ningûn veredicto
            if len(veredictos) == 0:
                return JSONResponse({"imageId": imageId, "telefono": telefono, "url_image":imageUrl})
            
            return JSONResponse(resultados)

        except KeyError as e:
            return send_errors(str(e),500, 'yolo_nas_test', 18)