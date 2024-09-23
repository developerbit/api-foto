import requests
from dotenv import load_dotenv
from load.services.env_service import get_enviroment
from utils.send_errors import send_errors

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def get_classes(id_etiquetas):
        try:
            # Obtener la URL del endpoint de la API desde las variables de entorno
            api_url_etiquetas = get_enviroment("API_URL_ETIQUETAS")
        
            # Concatenar el parámetro id_etiquetas a la URL del endpoint
            url_id = f"{api_url_etiquetas}/{id_etiquetas}"

            # Hacer la solicitud HTTP usando requests
            response = requests.get(url_id)

            if response.status_code == 200:
                
                # Decodificamos la respuesta JSON
                data = response.json()
                etiquetas = [objeto['nombre'] for objeto in data]

                return etiquetas

            else:
                # Manejar el caso en que la solicitud falle
                print("Error al obtener las clases desde la API:", response.status_code)
                raise KeyError(f"Error al obtener las clases desde la API:{api_url_etiquetas}/{id_etiquetas}")
                return []

        except KeyError as e:
            return send_errors(f"Error! no es posible obtener las clases desde FOTOSAPI {api_url_etiquetas}/{id_etiquetas}",500, 'get_etiquetas', 18)

