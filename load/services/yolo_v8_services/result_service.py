from utils.send_errors import send_errors    

class ResultService:

    @staticmethod
    def format_results(results, model, request_data):
        try:
            imageId = request_data['id_image']
            url_image = request_data['url_image']
            telefono = request_data.get('telefono', None)
            id_modelo = request_data['id_modelo']
            etiquetas = request_data.get('etiquetas', {})
            
            class_names = model.names  # Obtener nombres de clase
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

            logica = [{
                "id_modelo": id_modelo,
                "etiquetas": etiquetas
            }]

            resultados = {
                "imageId": imageId,
                "url_image": url_image,
                "telefono": telefono,
                "veredictos": veredictos,
                "logica": logica
            }

            return resultados
        except KeyError as e:
            return send_errors(str(e), 500, 'result_service', 13)
