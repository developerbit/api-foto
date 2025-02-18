import os
import requests
from dotenv import load_dotenv


# Cargar las variables de entorno desde el archivo .env
load_dotenv()
    
def send_errors(message,status_code,filename,line):
    ''''
    Esta funcion sirve para enviar los errores a la api principal de fotos y almacenarlos en la base de datos

    Args:
        message(string) Detalles del error
        status(string) estatus de la operacion
        filename(string) nombre del archivo actual 
        line(string) linea del archivo actual 
    '''
    # Obtener la URL del endpoint de la API desde las variables de entorno
    api_url_logs = os.getenv("API_URL_LOGS")
    x_api_key = os.getenv("X_API_KEY")
    app = os.getenv("APP_NOMBRE")
    data = {"message": message, "statusCode": status_code, "filename":filename, "app": app, "line":line}

    headers = {'x-api-key': x_api_key}
    response = requests.post(api_url_logs,data, headers)
    if response.status_code == 200:
        
        # Decodificamos la respuesta JSON
        data = response.json()

        return data
        #return response.json()
            #otro3
        #data = response.json()
        #return data['nombre']
    else:
        # Manejar el caso en que la solicitud falle
        print("Error al Enviar error:", response.status_code)
        return data
# Hacer la solicitud HTTP usando requests
