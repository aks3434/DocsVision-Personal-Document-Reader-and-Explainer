from fastapi import FastAPI
from docsvision.api.routes import upload, ask

app = FastAPI(
    title="DocsVision API",
    description="Document Intelligence API",
    version="0.1.0",
)

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(ask.router, prefix="/ask", tags=["Ask"])
