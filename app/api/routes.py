from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Document
from app.services.validators import validate_upload, validate_size
from app.services.storage import save_upload, infer_file_type

router = APIRouter()

@router.get("/health")
def health():
    return {"ok": True}

@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    ext = validate_upload(file)
    await validate_size(file)

    path = await save_upload(file)
    doc = Document(
        filename=file.filename,
        file_type=infer_file_type(ext),
        path=str(path),
        status="UPLOADED"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {
        "success": True,
        "document": {
            "id": doc.id,
            "filename": doc.filename,
            "file_type": doc.file_type,
            "status": doc.status
        }
    }
