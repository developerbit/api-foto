import os
import requests
from dotenv import load_dotenv


# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def get_modelo(id_modelo):
        # Obtener la URL del endpoint de la API desde las variables de entorno
        api_url_modelos = os.getenv("API_URL_MODELOS")
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
            return None
        else:
        # Manejar el caso en que la solicitud falle
            print("Error al obtener el modelo desde la API:", response.status_code)
            return None


