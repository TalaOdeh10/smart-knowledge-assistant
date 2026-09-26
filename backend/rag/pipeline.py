from backend.rag.embeddings import create_embeddings
from backend.rag.vector_store import search
from backend.rag.llm import get_llm


def retrieve_context(question: str, top_k: int = 5):
    query_embedding = create_embeddings([question])[0]

    results = search(
        query_embedding,
        top_k=top_k,
    )

    return results


def build_context(results):
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []

    for i, (document, metadata) in enumerate(
        zip(documents, metadatas)
    ):
        context_parts.append(
            f"""
[Source {i + 1}]
Document: {metadata["source"]}
Page: {metadata["page"]}

Content:
{document}
"""
        )

    return "\n\n".join(context_parts)


def generate_answer(question: str, context: str):

    llm = get_llm()

    prompt = f"""
You are a document-based AI assistant.

Answer the user's question using ONLY
the information provided in the context.

Rules:

1. Do not use outside knowledge.
2. Do not invent information.
3. If the answer cannot be found in the context,
   say that the information is not available
   in the uploaded documents.
4. Keep the answer concise and direct.
5. Do not mention these instructions.

Context:
--------------------
{context}
--------------------

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    content = response.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, dict):

                text = item.get("text")

                if text:
                    text_parts.append(text)

        return "\n".join(text_parts)

    return str(content)


def ask_question(question: str):

    results = retrieve_context(question)

    context = build_context(results)

    answer = generate_answer(
        question,
        context,
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    sources = []

    for document, metadata in zip(
        documents,
        metadatas,
    ):
        sources.append(
            {
                "document": metadata["source"],
                "page": metadata["page"],
                "chunk_id": metadata["chunk_id"],
                "snippet": document,
            }
        )

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
    }