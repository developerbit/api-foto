from  utils.send_errors import send_errors    
class ResultService:
    @staticmethod
    def format_results(df_prediccion, image_id, image_url, telefono, modelo, etiquetas):
        try:
            detalle_prediccion = df_prediccion.to_dict(orient="records")
            veredictos = [
                {
                    "imageId": image_id,
                    "classname": registro["classname"],
                    "yMin": registro["yMin"],
                    "xMin": registro["xMin"],
                    "yMax": registro["yMax"],
                    "xMax": registro["xMax"],
                }
                for registro in detalle_prediccion
            ]
            
            logica = [{"id_modelo": modelo, "etiquetas": etiquetas}]
            
            return {
                "imageId": image_id,
                "url_image": image_url,
                "telefono": telefono,
                "veredictos": veredictos,
                "logica": logica,
            }
        except KeyError as e:
            return send_errors(str(e),500, 'result_service', 18)
