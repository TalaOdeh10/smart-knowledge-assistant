import chromadb


client = chromadb.PersistentClient(
    path="backend/chroma_db"
)


collection = client.get_or_create_collection(
    name="documents"
)


def add_documents(
    chunks: list[str],
    embeddings,
    metadata: list[dict],
):
    ids = []

    for item in metadata:
        document_id = item["document_id"]
        chunk_id = item["chunk_id"]

        ids.append(
            f"{document_id}_chunk_{chunk_id}"
        )

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadata,
    )


def search(
    query_embedding,
    top_k: int = 5,
):
    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    return results

def delete_document(document_id: str):
    results = collection.get(
        where={
            "document_id": document_id
        }
    )

    ids = results["ids"]

    if ids:
        collection.delete(ids=ids)