import os
from PIL import Image
from load.model.util import Util
from  utils.send_errors import send_errors    

class ImageService:
    
    @staticmethod
    def process_image(url_image):
        try:
            file_name = Util.Download(os.getenv('UPLOAD_FOLDER_IMAGENES'), url_image)
            return file_name
        except KeyError as e:
            return send_errors(str(e),500, 'process_image', 13)

    @staticmethod
    def load_image(file_name):
        try:
            image = Image.open(file_name)
            return image
        except Exception as e:
            return send_errors(str(e), 500, 'load_image', 13)
