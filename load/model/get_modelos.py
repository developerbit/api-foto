import requests
from dotenv import load_dotenv
from load.services.env_service import get_enviroment
from  utils.send_errors import send_errors    

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def get_modelo(id_modelo):
        try:
            # Obtener la URL del endpoint de la API desde las variables de entorno
            api_url_modelos = get_enviroment("API_URL_MODELOS")
            print(api_url_modelos)
            # Concatenar el parámetro id_etiquetas a la URL del endpoint
            url_id = f"{api_url_modelos}/{id_modelo}"

            # Hacer la solicitud HTTP usando requests
            response = requests.get(url_id)

            if response.status_code == 200:
                
                # Decodificamos la respuesta JSON
                data = response.json()
                # Verificar si se encontró un objeto con el ID especificado
                if data and 'nombre' in data:
                    return data['nombre']
            else:
                print("No se encontró un modelo con el ID especificado:", id_modelo)
                raise KeyError("No se encontró un modelo con el ID especificado:", id_modelo)
        
        except KeyError as e:
            return send_errors(f"No se encontró un modelo con el ID especificado: {id_modelo}",500, 'get_modelos', 18)