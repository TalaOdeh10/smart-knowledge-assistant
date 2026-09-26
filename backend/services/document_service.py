#The service becomes the orchestrator.

from pathlib import Path

from backend.rag.loader import load_document
from backend.rag.chunker import split_text
from backend.rag.embeddings import create_embeddings
from backend.rag.vector_store import add_documents


def process_document(
    file_path: str,
    document_id: str,
    original_filename: str | None = None,
):

    file_name = (
        original_filename
        if original_filename
        else Path(file_path).name
    )

    # -----------------------------------------
    # 1. Load document
    # -----------------------------------------

    pages = load_document(file_path)

    all_chunks = []
    metadata = []

    # -----------------------------------------
    # 2. Process every page
    # -----------------------------------------

    global_chunk_index = 0

    for page in pages:

        chunks = split_text(
            page["text"],
            chunk_size=200,
            chunk_overlap=40,
        )

        for chunk in chunks:

            all_chunks.append(chunk)

            metadata.append(
                {
                    "document_id": document_id,
                    "source": file_name,
                    "page": page["page"],
                    "chunk_id": global_chunk_index,
                }
            )

            global_chunk_index += 1

    if not all_chunks:

        raise ValueError(
            "No text could be extracted from the document."
        )

    # -----------------------------------------
    # 3. Create embeddings
    # -----------------------------------------

    embeddings = create_embeddings(
        all_chunks
    )

    # -----------------------------------------
    # 4. Store in Chroma
    # -----------------------------------------

    add_documents(
        chunks=all_chunks,
        embeddings=embeddings,
        metadata=metadata,
    )

    return {
        "document_id": document_id,
        "filename": file_name,
        "chunks": len(all_chunks),
    }