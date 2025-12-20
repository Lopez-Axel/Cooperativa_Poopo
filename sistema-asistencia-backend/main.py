from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import api_router
from database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Asistencia Cooperativa",
    description="API para gestión de asistencia con QR",
    version="2.0.0",
    redirect_slashes=False
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API Sistema de Asistencia", "version": "2.0.0"}