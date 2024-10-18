from fastapi import Request
from fastapi.responses import JSONResponse
#from load.model.pattern import Pattern
from load.model.yolo_nas import ModeloYoloNas
from load.model.yolov8 import ModeloYoloV8

class ModeloMain:
    async def Mision(self,request: Request):
        
        try:
            return await ModeloYoloV8().AnalyzeModel(request)
            #return "<h1>Estas en el endpoint Misiones </h1>"
        except Exception as ex:
            error_message = getattr(ex, 'description', str(ex))
            return JSONResponse(content={"error": error_message}, status_code=500)
        
    async def Mision_test(self,request: Request):
        
        try:
            return await ModeloYoloNas().AnalyzeModel_test(request)
            #return "<h1>Estas en el endpoint Misiones </h1>"
        except Exception as ex:
            error_message = getattr(ex, 'description', str(ex))
            return JSONResponse(content={"error": error_message}, status_code=500)    