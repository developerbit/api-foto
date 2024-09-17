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
    app = os.getenv("APP_NAME")
    data = {"message": message, "statusCode": status_code, "filename":filename, "app": app}
    response = requests.post(api_url_logs,data)
    # Hacer la solicitud HTTP usando requests
