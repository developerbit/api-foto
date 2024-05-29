
import os
from dotenv import load_dotenv
from load.model.util import Util
from load.model.verdict import Verdict
from fastapi.responses import JSONResponse
from fastapi import Request
load_dotenv()


class Pattern:
    
    async def AnalyzeModel2(self,request: Request):
        
        # Imprimir el contenido de los datos JSON en la consola
        data = await request.json()
        print(data)
        #image='https://ventolini.com/wp-content/uploads/2023/04/gaseosa1.jpg'
        #datafv='FV'

        file_name = Util.Download(os.environ.get('UPLOAD_FOLDER_POSTOBON'), data['url_image'])
        print(file_name)    

        fv = data['fv'].upper()
        etiquetas = data['etiquetas']
        #print(etiquetas)
        weights = os.environ.get('MODELOPT')
        source = file_name
        imgsz = 640
        conf_thres = 0.25
        labels, time, coordinates = Util.Analyze(weights, source, imgsz, conf_thres)
        
        #CODIGO YOLO_NAS
        #prediction=Util.Analyze_yolo_nas(prediction)
        #print(prediction)
        
        if not labels:
            return {
                "code": 1,
                "message": "La imagen no contiene objetos detectados",
                "labels": labels,
                "time": time,
                "coordinates": coordinates,
                "verdict": 0,
                "explanation": "La imagen no contiene objetos detectados",
                "version": "v7 26/05/2021"
            }

        Util.RemoveImage(file_name)

        # Calcular la cantidad para cada etiqueta
        cantidad_etiquetas = {}
        for etiqueta in etiquetas:
            cantidad_etiquetas[etiqueta] = Util.QuantityElement(coordinates, etiqueta)

        # Calcular la cantidad total
        quantity = sum(cantidad_etiquetas.values())


        #Logica de negocio
        verdict, explanation = Verdict.LogicaNegocio(quantity,cantidad_etiquetas,etiquetas)

        return {
            "code": 1,
            "message": "Imagen analizada correctamente",
            "labels": labels,
            "time": time,
            "coordinates": coordinates,
            "verdict": verdict,
            "explanation": explanation,
            "version": "v7 26/05/2021"
        }
