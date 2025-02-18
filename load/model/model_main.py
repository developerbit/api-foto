from fastapi import Request
from fastapi.responses import JSONResponse
#from load.model.pattern import Pattern
from load.model.yolo_nas import ModeloYoloNas
from load.model.yolov8 import ModeloYoloV8
from load.services.env_service import get_enviroment

class ModeloMain:
    async def Mision(self,request: Request):

        try:
            data = await request.json()
            empresa =  data['empresa_id_celuweb']
            # id_modelo = int(data['id_modelo'])
            # modulo = int(data['modulo'])
            # return id_modelo
            modelsFolder = get_enviroment('FOLDER_MODEL');
            modelRoute = data['empresa_id_celuweb']
            modelos =  data['modelos']
            inferencias = []
            counter = 0
            for m in modelos:
                inferencia =  await ModeloYoloV8().AnalyzeModel(request, m, empresa)
                counter += 1
                inferencias.append({counter: inferencia})
                # return i 
            # return JSONResponse(content = { 'result': inferencias }, status_code=200)
            return inferencias
            # error_message = getattr(ex, 'description', str(ex))
                # return JSONResponse(content={"error": error_message}, status_code=500)
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
