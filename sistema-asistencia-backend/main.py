from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import cooperativistas
from routers import attendance
from routers import devices
from routers import users
from routers import config
from routers import auth
from routers import attendance_period
from routers import upload
app = FastAPI(
    title="Sistema de Asistencia - Cooperativa",
    description="API para gestión de asistencia de cooperativistas",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas (opcional, mejor usar init_db.py)
# Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {
        "message": "API Sistema de Asistencia - Cooperativa",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Registrar routers (cuando los creemos)
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(cooperativistas.router, prefix="/api", tags=["cooperativistas"])
app.include_router(devices.router, prefix="/api", tags=["devices"])
app.include_router(attendance.router, prefix="/api", tags=["attendance"])
app.include_router(config.router, prefix="/api", tags=["config"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(attendance_period.router, prefix="/api", tags=["attendance-periods"])
app.include_router(upload.router, prefix="/api", tags=["uploads"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
