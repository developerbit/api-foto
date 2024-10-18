from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import APIRouter,Request
from load.model.model_main import ModeloMain
#from load.seasons.postobon.main import PostobonMain
#from load.auth.main import AuthMain

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def index():
    return "<h1>API IA version 2 esta funcionando</h1>"

@router.post("/api/user/auth", response_class=JSONResponse)
def auth():
    # Lógica de autenticación
    return {"message": "Authentication endpoint"}


@router.post("/ia/mision")
async def Reconocimiento(request: Request):
    return await ModeloMain().Mision(request)


@router.post("/ia/mision/test")
async def Reconocimiento_test(request: Request):
    return await ModeloMain().Mision_test(request)
# Define el resto de tus rutas aquí...

def configure_routes(app):
    app.include_router(router, prefix="")
