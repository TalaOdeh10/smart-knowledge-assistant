from datetime import datetime, timezone

from sqlmodel import SQLModel, Field


class Document(SQLModel, table=True):

    id: str = Field(primary_key=True)

    filename: str

    file_type: str

    status: str = "processing"

    chunk_count: int = 0

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )