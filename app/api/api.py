from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
import os
import uuid
import logging
import aiofiles
from app.src.audio_processing import (
    reduce_noise,
    apply_bandpass_filter,
    normalize_volume
)

router = APIRouter()
logger = logging.getLogger(__name__)

async def handle_audio_processing(file: UploadFile, processing_func, **kwargs):
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
        output_filename = f"processed_{unique_id}.wav"
        output_path = os.path.join(output_dir, output_filename)

        # Async file writing
        async with aiofiles.open(temp_path, "wb") as buffer:
            content = await file.read()
            await buffer.write(content)

        # Process audio
        processing_func(temp_path, output_path, **kwargs)

        # Cleanup
        os.remove(temp_path)

        return JSONResponse(
            content={"processed_file": f"/output/{output_filename}"}
        )

    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/noise-reduction/", summary="Apply noise reduction")
async def noise_reduction(
    file: UploadFile = File(...),
    reduction_strength: float = Query(0.5, ge=0.1, le=1.0)
):
    """
    Apply noise reduction to audio file
    
    - **reduction_strength**: Noise reduction strength (0.1 to 1.0)
    """
    return await handle_audio_processing(
        file, 
        reduce_noise,
        reduction_strength=reduction_strength
    )

@router.post("/bandpass-filter/", summary="Apply bandpass filter")
async def bandpass_filter(
    file: UploadFile = File(...),
    lowcut: int = Query(300, ge=20, le=20000),
    highcut: int = Query(3400, ge=20, le=20000)
):
    """
    Apply Butterworth bandpass filter
    
    - **lowcut**: Low cutoff frequency (Hz)
    - **highcut**: High cutoff frequency (Hz)
    """
    return await handle_audio_processing(
        file,
        apply_bandpass_filter,
        lowcut=lowcut,
        highcut=highcut
    )

@router.post("/normalize-volume/", summary="Normalize audio volume")
async def normalize_audio_volume(
    file: UploadFile = File(...),
    target_dBFS: float = Query(-20.0, ge=-30.0, le=0.0)
):
    """
    Normalize audio volume
    
    - **target_dBFS**: Target volume level in dBFS
    """
    return await handle_audio_processing(
        file,
        normalize_volume,
        target_dBFS=target_dBFS
    )