# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.logger import logger
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.services.ml_models import MLModelManager
from app.services.voice_parser import VoiceCommandParser
from app.api import auth, transactions, students, teachers, management, voice

ml_manager = MLModelManager()
voice_parser = VoiceCommandParser()

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        ml_manager.train_performance_model(db)
        ml_manager.train_dropout_model(db)
        ml_manager.train_revenue_model(db)
        logger.info("ML models trained successfully")
    except Exception as e:
        logger.error(f"Error training models: {e}")
    finally:
        db.close()
    yield
    logger.info("Application shutdown")

app = FastAPI(
    title="School Management Backend API",
    description="Backend system for report generation and predictive analytics",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(management.router)
app.include_router(voice.router)