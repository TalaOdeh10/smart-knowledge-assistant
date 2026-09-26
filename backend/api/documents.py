from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException
from sqlmodel import Session, select

from backend.database import engine
from backend.models.document import Document
from backend.services.document_service import process_document
from backend.rag.vector_store import delete_document as delete_vectors


router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"],
)


UPLOAD_DIR = Path("backend/data/documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


ALLOWED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx",
}


@router.get("")
def get_documents():
    """
    Return all documents stored in SQLite.
    """

    with Session(engine) as session:

        statement = select(Document).order_by(
            Document.created_at.desc()
        )

        documents = session.exec(statement).all()

        return documents


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
):
    try:

        # -----------------------------------------
        # Validate filename
        # -----------------------------------------

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No filename provided.",
            )

        original_filename = Path(
            file.filename
        ).name

        extension = Path(
            original_filename
        ).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type.",
            )

        # -----------------------------------------
        # Generate unique document ID
        # -----------------------------------------

        document_id = str(uuid4())

        # -----------------------------------------
        # Save uploaded file
        # -----------------------------------------

        file_path = (
            UPLOAD_DIR
            / f"{document_id}_{original_filename}"
        )

        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        with open(file_path, "wb") as output:
            output.write(contents)

        # -----------------------------------------
        # Create SQLite document record
        # -----------------------------------------

        document = Document(
            id=document_id,
            filename=original_filename,
            file_type=extension,
            status="processing",
            chunk_count=0,
        )

        with Session(engine) as session:

            session.add(document)
            session.commit()

        # -----------------------------------------
        # Process + index document
        # -----------------------------------------

        try:

            result = process_document(
                file_path=str(file_path),
                document_id=document_id,
            )

        except Exception:

            # Mark document as failed
            with Session(engine) as session:

                failed_document = session.get(
                    Document,
                    document_id,
                )

                if failed_document:

                    failed_document.status = "failed"

                    session.add(failed_document)
                    session.commit()

            raise

        # -----------------------------------------
        # Update SQLite record
        # -----------------------------------------

        with Session(engine) as session:

            saved_document = session.get(
                Document,
                document_id,
            )

            if saved_document:

                saved_document.status = "indexed"

                saved_document.chunk_count = result[
                    "chunks"
                ]

                session.add(saved_document)
                session.commit()

                session.refresh(saved_document)

                document_response = saved_document

            else:

                raise HTTPException(
                    status_code=500,
                    detail="Document record was not found.",
                )

        # -----------------------------------------
        # Return response
        # -----------------------------------------

        return {
            "message": (
                "Document uploaded and indexed successfully."
            ),
            "document": document_response,
        }

    except HTTPException:
        raise

    except Exception as e:

        print(
            "UPLOAD ERROR:",
            repr(e),
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"{type(e).__name__}: {str(e)}"
            ),
        )


@router.delete("/{document_id}")
def delete_document(document_id: str):

    # -----------------------------------------
    # Find document in SQLite
    # -----------------------------------------

    with Session(engine) as session:

        document = session.get(
            Document,
            document_id,
        )

        if not document:

            raise HTTPException(
                status_code=404,
                detail="Document not found.",
            )

        filename = document.filename

        # -----------------------------------------
        # Delete vectors from Chroma
        # -----------------------------------------

        delete_vectors(document_id)

        # -----------------------------------------
        # Delete physical file
        # -----------------------------------------

        matching_files = list(
            UPLOAD_DIR.glob(
                f"{document_id}_*"
            )
        )

        for file_path in matching_files:

            if file_path.exists():
                file_path.unlink()

        # -----------------------------------------
        # Delete SQLite record
        # -----------------------------------------

        session.delete(document)
        session.commit()

    return {
        "message": "Document deleted successfully.",
        "document_id": document_id,
        "filename": filename,
    }