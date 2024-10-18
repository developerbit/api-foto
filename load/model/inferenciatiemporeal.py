import cv2
import torch
from ultralytics import YOLO

# Ruta al modelo .pt y la imagen
MODEL_PATH = r'C:\Users\juana\Desktop\Unificar Trabajo Modelos\Investigacion\Api_para_leer.pt\api-foto - copia\models\pt\YUPI.pt'
IMAGE_PATH = r'C:\Users\juana\Desktop\pr3.jpg'

# Cargar el modelo
model = YOLO(MODEL_PATH)

# Leer la imagen con OpenCV
image = cv2.imread(IMAGE_PATH)

# Realizar la inferencia usando el modelo
results = model(image)

# Obtener el mapeo de nombres de clases del modelo
class_names = model.names

# Dibujar los bounding boxes en la imagen
for result in results:
    for box, class_idx in zip(result.boxes.xyxy, result.boxes.cls):
        # Obtener coordenadas del bounding box
        x_min = int(box[0].item())
        y_min = int(box[1].item())
        x_max = int(box[2].item())
        y_max = int(box[3].item())

        # Convertir índice de clase a entero y obtener el nombre de la clase
        class_idx = int(class_idx.item())
        class_name = class_names.get(class_idx, "Desconocido")

        # Dibujar el bounding box en la imagen
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        # Poner el nombre de la clase encima del bounding box
        cv2.putText(image, class_name, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Mostrar la imagen con los bounding boxes
cv2.imshow("Detecciones", image)

# Esperar a que se presione una tecla y cerrar la ventana
cv2.waitKey(0)
cv2.destroyAllWindows()

# Opcional: Guardar la imagen resultante en disco
cv2.imwrite("resultado_detecciones.jpg", image)
