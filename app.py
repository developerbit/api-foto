from fastapi import FastAPI
from load.url import configure_routes
#from dotenv import load_dotenv
import os

#load_dotenv()

app = FastAPI()

configure_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
