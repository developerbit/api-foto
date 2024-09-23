import os
from dotenv import load_dotenv
load_dotenv()
from load.model.util import Util
from cv2 import imread
import cv2
from load.services.env_service import get_enviroment
from  utils.send_errors import send_errors    

# def cargar_imagen(image_file):


def process_image(url_image):
    try:
        image_file = Util.Download(get_enviroment('UPLOAD_FOLDER_IMAGENES'), url_image)
        return image_file
    except KeyError as e:
        return send_errors(str(e),500, 'process_image', 13)
    
def cargar_image(image_file):
    try:
        img = imread(image_file)
        if img is None:
            raise ValueError("No se pudo cargar la imagen desde la ruta especificada:", image_file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img
    except KeyError as e:
        return send_errors(str(e),500, 'process_image', 13)