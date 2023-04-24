from fastapi import FastAPI
from routers.routes import router as coderouter

app = FastAPI(title="VerifiedProof API",
              docs_url="/",
              )
app.include_router(coderouter)
