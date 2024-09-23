from  utils.send_errors import send_errors    

class VeredictoService:

    def jsonVeredict(detalle_prediccion,imageId,id_modelo,etiquetas,imageUrl,telefono):
        try:
            for registro in detalle_prediccion:
                veredictos = []
                veredicto = {
                    "imageId": imageId,
                    "classname": registro["classname"],
                    "yMin": registro["yMin"],
                    "xMin": registro["xMin"],
                    "yMax": registro["yMax"],
                    "xMax": registro["xMax"],
                }
                veredictos.append(veredicto)

            #crear la lôgica para el veredicto basado en etiquetas 
            logica = [{
                "id_modelo": id_modelo,
                "etiquetas": etiquetas
            }]
            
            #   crear el diccionario de resultados
            resultados = {
                "imageId": imageId,
                "url_image": imageUrl,
                "telefono": telefono,
                "veredictos": veredictos,
                "logica": logica,
            }
            return veredictos,  resultados
        except KeyError as e:
            return send_errors(str(e),500, 'veredicto_service', 18)
