from utils.send_errors import send_errors    

class VeredictoService:

    @staticmethod
    def format_veredict(detalle_prediccion, imageId, id_modelo, etiquetas, imageUrl, telefono):
        try:
            veredictos = []
            for registro in detalle_prediccion:
                veredicto = {
                    "imageId": imageId,
                    "classname": registro["classname"],
                    "yMin": registro["yMin"],
                    "xMin": registro["xMin"],
                    "yMax": registro["yMax"],
                    "xMax": registro["xMax"],
                }
                veredictos.append(veredicto)

            logica = [{
                "id_modelo": id_modelo,
                "etiquetas": etiquetas
            }]

            resultados = {
                "imageId": imageId,
                "url_image": imageUrl,
                "telefono": telefono,
                "veredictos": veredictos,
                "logica": logica
            }

            return veredictos, resultados
        except KeyError as e:
            return send_errors(str(e),500, 'veredicto_service', 13)
