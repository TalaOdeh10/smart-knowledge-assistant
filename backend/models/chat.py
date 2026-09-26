from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class Source(BaseModel):
    document: str
    page: int
    chunk_id: int
    snippet: str


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[Source]