from fastapi import FastAPI
from routers.routes import router as coderouter
app = FastAPI()
app.include_router(coderouter)
