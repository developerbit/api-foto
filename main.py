from fastapi import FastAPI
from load.url import configure_routes  # 👈 IMPORTANTE

app = FastAPI()
configure_routes(app)  #REGISTRA LAS RUTAS DEL PROYECTO

@app.get("/")
def read_root():
    return {"message": "Hello, World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
