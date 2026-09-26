from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from backend.api.documents import router as documents_router
from backend.api.chat import router as chat_router
from backend.database import create_db_and_tables


app = FastAPI(
    title="Smart Knowledge Assistant",
    description="A production-style RAG knowledge assistant",
    version="1.0.0",
)

create_db_and_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(documents_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "Smart Knowledge Assistant API is running!"
    }