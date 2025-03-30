from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
import logging
from app.src.audio_processing import process_audio
import aiofiles



router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/process-audio/", summary="Process audio file")
async def process_audio_endpoint(file: UploadFile = File(...)):
    try:
        # Validate file format
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ('.wav', '.mp3'):
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Only WAV and MP3 are allowed."
            )

        # Create directories
        unique_id = uuid.uuid4().hex
        temp_dir = "data/temp"
        output_dir = "data/output"
        os.makedirs(temp_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)

        # Save temporary file
        temp_path = os.path.join(temp_dir, f"temp_{unique_id}{file_ext}")
        async with aiofiles.open(temp_path, "wb") as buffer:
            content = await file.read()
            await buffer.write(content)

        # Process audio
        output_filename = f"processed_{unique_id}.wav"
        output_path = os.path.join(output_dir, output_filename)
        process_audio(temp_path, output_path)

        # Cleanup
        os.remove(temp_path)

        return JSONResponse(
            content={"processed_file": f"/output/{output_filename}"}
        )

    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))