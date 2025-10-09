# app/main.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.routers import auth, users, companies, permissions, orders

# Configuración
from app.config import ALLOWED_ORIGINS  # lista de dominios permitidos para CORS, ej: ["*"]

app = FastAPI(title="dacazMD webCliente", version="1.0.0")

# -------------------------
# CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Endpoints raíz de prueba
# -------------------------
@app.get("/")
def root():
    return {"message": "dacazMD webCliente funcionando correctamente"}

# -------------------------
# Incluir Routers
# -------------------------
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(companies.router)
app.include_router(permissions.router)
app.include_router(orders.router)
