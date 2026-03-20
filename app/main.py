from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from app import crud, models, schemas
from app.database import SessionLocal, engine
from app.chat import procesar_pregunta

# Crear tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints Usuarios ---
@app.post("/usuarios/", response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.create_usuario(db=db, usuario=usuario)

@app.get("/usuarios/", response_model=list[schemas.Usuario])
def read_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_usuarios(db, skip=skip, limit=limit)

@app.get("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario(db, usuario_id=usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return db_usuario

# --- Endpoints Preguntas/Chat ---
@app.post("/api/ask")
def ask_api(pregunta_data: schemas.Pregunta, db: Session = Depends(get_db)):
    pregunta = pregunta_data.message
    respuesta = procesar_pregunta(pregunta, db)
    return {"reply": respuesta}

@app.get("/api/ask")
def ask_invalid():
    return {"error": "Usa POST para enviar preguntas"}

'''# --- Startup event: opcional ---
@app.on_event("startup")
def startup_usuario_prueba():
    db = next(get_db())
    if not crud.get_usuarios(db):
        usuario = schemas.UsuarioCreate(
            user_name="Mariatchi",
            email=None,
            telefono=None,
            direccion="Carrer de la Música, 12, Barcelona"
        )
        user_db = crud.create_usuario(db, usuario)
        crud.create_evento(db, schemas.EventoCreate(
            nombre="Concierto Mariatchi",
            fecha_hora=datetime.utcnow(),
            local_id=user_db.id
        ))'''
