import torch

# Ruta del modelo
model_path = r'C:\Users\juana\Desktop\Unificar Trabajo Modelos\Investigacion\Api_para_leer.pt\api-foto - copia\models\pt\YUPI.pt'


# Cargar el modelo y acceder a las clases
try:
    model_data = torch.load(model_path, map_location='cpu')

    # Verificar si hay información sobre las clases en el objeto del modelo
    model_structure = model_data.get('model', None)
    if model_structure:
        if hasattr(model_structure, 'names'):
            # Las clases suelen estar en un atributo 'names' o similar
            classes = model_structure.names
            print("Clases del modelo:", classes)
        else:
            print("No se encontraron nombres de clases directamente en el modelo.")
    else:
        print("La clave 'model' no contiene una estructura accesible.")

except Exception as e:
    print("Error al acceder a las clases del modelo:", str(e))
