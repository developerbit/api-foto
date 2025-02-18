from utils.send_errors import send_errors    
from load.services.env_service import get_enviroment
from fastapi.encoders import jsonable_encoder

class ResultService:

    @staticmethod
    def format_results(results, model, request_data):
        try:
            imageId = request_data['id_image']
            url_image = request_data['url_image']
            telefono = request_data.get('telefono', None)
            # id_modelo = request_data['id_modelo']
            modulo = request_data['modulo']
            etiquetas = request_data['etiquetas']

            class_names = model.names  # Obtener nombres de clase
            veredictos = []
            total_reconocido = 0
            for result in results:
                for box, class_idx in zip(result['bbox'], result['class_name']):
                    total_reconocido += 1
                    class_name =result['class_name'] 
                    veredicto = {
                            "imageId": imageId,
                            "classname": class_name,
                            "xMin": box[0],
                            "yMin": box[1],
                            "xMax": box[2],
                            "yMax": box[3]
                            }
                    veredictos.append(veredicto)
                    # return veredictos

            logica = [{
                # "id_modelo": id_modelo,
                "id_modulo": modulo,
                "etiquetas": etiquetas
                }]

            resultados = {
                    "imageId": imageId,
                    "url_image": url_image,
                    "telefono": telefono,
                    "veredictos": veredictos,
                    "logica": logica,
                    "modulo": modulo,
                    "total_productos": total_reconocido
                    }

            return resultados
        except KeyError as e:
            return send_errors(str(e), 500, 'result_service', 13)


    @staticmethod
    def total_result(results):
        try:

            total = 0

            for result in results:
                for box, class_idx in zip(result.boxes.xyxy, result.boxes.cls):
                    total += 1 
                # for box, class_idx in zip(result.boxes.xyxy, result.boxes.cls):

            return total
        except KeyError as e:
            return send_errors(str(e), 500, 'result_service', 13)


