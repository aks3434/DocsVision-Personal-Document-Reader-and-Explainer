from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile
import shutil
from pathlib import Path

from docsvision.scripts.ingest import main as ingest_main

router = APIRouter()

@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".json"):
        raise HTTPException(
            status_code=400,
            detail="Only parsed JSON files are supported for now."
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = Path(tmp.name)

    try:
        ingest_main(str(tmp_path))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}"
        )

    return {
        "status": "success",
        "message": "Document uploaded and indexed successfully"
    }
