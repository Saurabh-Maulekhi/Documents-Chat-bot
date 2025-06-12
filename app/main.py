from fastapi import FastAPI
from app.api.document_api import router as docs_router

app = FastAPI()
app.include_router(docs_router, prefix="/docs")



