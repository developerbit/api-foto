import torch
from super_gradients.training import models
from load.model.get_etiquetas import get_classes
from load.model.get_modelos import get_modelo
from load.services.env_service import get_enviroment
from  utils.send_errors import send_errors    

"""
Buscador de variables.

Args:
    id_modelo: Id de modelo en base de datos 
"""
@staticmethod
def load_model( modelo,id_modelo = None ):
    try:
        num_classes = 0
        if(id_modelo != None):
            classes = get_classes(id_modelo)
            num_classes = len(classes)

        model_path = get_enviroment(modelo)
        model = models.get(
                'yolo_nas_m',
                pretrained_weights="coco",
                num_classes=num_classes,
                checkpoint_path=model_path
                )
        device = "mps" if torch.backends.mps.is_available() else "cpu"
        return model.to(device), classes, device
    except KeyError as e:
        return send_errors(f"Error al cargar modelos, model_path: {model_path}, device: {device}, si model_path y device se muestran correctamente, el error esta en las clases",500, 'get_modelos', 18)
