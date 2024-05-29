import os
import requests
from dotenv import load_dotenv


# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def get_classes(id_etiquetas):
        # Obtener la URL del endpoint de la API desde las variables de entorno
        api_url_etiquetas = os.getenv("API_URL_ETIQUETAS")
       
        # Concatenar el parámetro id_etiquetas a la URL del endpoint
        url_id = f"{api_url_etiquetas}/{id_etiquetas}"

        # Hacer la solicitud HTTP usando requests
        response = requests.get(url_id)

        if response.status_code == 200:
            
            # Decodificamos la respuesta JSON
            data = response.json()
            etiquetas = [objeto['nombre'] for objeto in data]

            return etiquetas
            #return response.json()
             #otro3
            #data = response.json()
            #return data['nombre']
        else:
            # Manejar el caso en que la solicitud falle
            print("Error al obtener las clases desde la API:", response.status_code)
            return []


