import os
from fastapi.responses import JSONResponse
from fastapi import Request
from dotenv import load_dotenv
from PIL import Image
from load.model.util import Util
from ultralytics import YOLO

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class ModeloYoloV8:
    def __init__(self):
        # Diccionario que mapea los id_modelo a sus respectivas rutas de archivo .pt
        self.model_paths = {
            3: os.getenv('YUPI'),
            5: os.getenv('RAMO'),
            9: os.getenv('KOALA')
        }
        self.models = {}

    # Método para cargar el modelo en función del id_modelo
    def cargar_modelo(self, id_modelo):
        if id_modelo in self.models:
            return self.models[id_modelo]  # Devuelve el modelo si ya ha sido cargado previamente
        elif id_modelo in self.model_paths:
            modelo = YOLO(self.model_paths[id_modelo])  # Cargar el modelo correspondiente
            self.models[id_modelo] = modelo  # Almacenar el modelo en caché
            return modelo
        else:
            raise ValueError(f"No se encontró un modelo para el id_modelo: {id_modelo}")

    async def AnalyzeModel(self, request: Request):
        try:
            # Extraer los datos de la solicitud
            data = await request.json()
            id_modelo = int(data['id_modelo'])  # Convertir a entero para evitar errores

            # Cargar el modelo basado en el id_modelo
            try:
                model = self.cargar_modelo(id_modelo)
            except ValueError as e:
                return JSONResponse(content={"error": str(e)}, status_code=400)

            # Descargar la imagen desde la URL proporcionada
            try:
                file_name = Util.Download(os.getenv('UPLOAD_FOLDER_IMAGENES'), data['url_image'])
            except Exception as e:
                return JSONResponse(content={"error": f"Error al descargar la imagen: {str(e)}"}, status_code=500)

            # Realizar la inferencia utilizando el modelo cargado
            try:
                image = Image.open(file_name)  # Cargar la imagen
                results = model(image)  # Realizar la inferencia

                # Verificar que el modelo devuelve resultados
                if not results:
                    return JSONResponse(content={"error": "No se encontraron resultados en la imagen."}, status_code=500)

                # Formatear y devolver la respuesta de la inferencia
                formatted_json = await self.formatear_respuesta(results, model, data)
                return JSONResponse(content=formatted_json, status_code=200)

            except Exception as e:
                return JSONResponse(content={"error": f"Error al realizar la inferencia: {str(e)}"}, status_code=500)

        except Exception as e:
            return JSONResponse(content={"error": f"Error en el proceso de inferencia: {str(e)}"}, status_code=500)

    # Método para formatear la respuesta de la inferencia
    async def formatear_respuesta(self, results, model, request_data):
        imageId = request_data['id_image']
        url_image = request_data['url_image']
        telefono = request_data.get('telefono', None)
        id_modelo = request_data['id_modelo']
        etiquetas = request_data.get('etiquetas', {})

        # Obtener el mapeo de nombres de clases del modelo
        class_names = model.names  # Esto debería ser un diccionario de índice a nombre de clase

        # Extraer los resultados de detección
        veredictos = []
        for result in results:
            for box, class_idx in zip(result.boxes.xyxy, result.boxes.cls):
                class_idx = int(class_idx.item())  # Convertir el índice de clase a entero
                class_name = class_names.get(class_idx, "Desconocido")  # Obtener el nombre de la clase
                veredicto = {
                    "imageId": imageId,
                    "classname": class_name,
                    "yMin": box[1].item(),
                    "xMin": box[0].item(),
                    "yMax": box[3].item(),
                    "xMax": box[2].item()
                }
                veredictos.append(veredicto)

        # Formatear la respuesta
        formatted_response = {
            "imageId": imageId,
            "url_image": url_image,
            "telefono": telefono,
            "veredictos": veredictos,
            "logica": [
                {
                    "id_modelo": id_modelo,
                    "etiquetas": etiquetas
                }
            ]
        }

        return formatted_response
