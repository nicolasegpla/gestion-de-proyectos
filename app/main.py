from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from app.routers import auth_empresa, usuarios, proyectos, historias_usuario, tickets

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://prueba-tecnica-gestion-proyectoss.s3-website-us-east-1.amazonaws.com",
        "http://localhost:5173",     # Para desarrollo local
    ],  # o ["*"] si estás en desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
async def test(request: Request):
    print("Origin: ", request.headers.get("origin"))
    print("IP: ", request.client.host if request.client else "No client")
    return {"message": "Hola no mas cartera API!"}

app.include_router(auth_empresa.router, prefix="/auth", tags=["Autenticación Empresa"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(proyectos.router, prefix="/proyectos", tags=["Proyectos"])
app.include_router(historias_usuario.router, prefix="/historias-usuario", tags=["Historias de Usuario"])
app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])
