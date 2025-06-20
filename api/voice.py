# app/api/voice.py

from fastapi import APIRouter
from app.services.voice_parser import VoiceCommandParser
from app.core.logger import logger

router = APIRouter(prefix="/voice", tags=["Voice"])

voice_parser = VoiceCommandParser()

@router.post("/interpret")
def interpret_voice(command: str):
    result = voice_parser.parse_voice_command(command)
    logger.info(f"Voice command interpreted: {result}")
    return result
