# 🧠 Smart Knowledge Assistant

A full-stack Retrieval-Augmented Generation (RAG) application that allows users to upload documents and interact with their knowledge through a web-based AI assistant.

The system processes uploaded documents, creates semantic embeddings, stores them in a vector database, retrieves relevant content for each question, and generates grounded answers using an LLM.

## ✨ Features

* 📄 Upload PDF, DOCX, and TXT documents
* ✂️ Document text extraction and chunking
* 🧠 Semantic embeddings using Sentence Transformers
* 🗄️ Persistent vector storage with ChromaDB
* 🔎 Semantic similarity retrieval
* 🤖 LLM-powered grounded answers
* 📚 Source attribution with document and page information
* 📂 Document management
* ⚡ FastAPI backend
* 🌐 Web-based chat interface
* 🧪 Retrieval evaluation
* ✅ Automated tests
* 🗃️ SQLite document metadata database

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │    Web Frontend     │
                    │                     │
                    │ Upload Documents    │
                    │ Chat Interface      │
                    │ View Sources        │
                    └──────────┬──────────┘
                               │
                              HTTP
                               │
                               ↓
                    ┌─────────────────────┐
                    │       FastAPI       │
                    │                     │
                    │ Document API        │
                    │ Chat API            │
                    └──────────┬──────────┘
                               │
                               ↓
                    ┌─────────────────────┐
                    │    RAG Pipeline     │
                    │                     │
                    │ Load → Chunk        │
                    │ Embed → Retrieve    │
                    │ → Generate          │
                    └───────┬─────┬───────┘
                            │     │
                            ↓     ↓
                    ┌──────────┐ ┌──────────┐
                    │ ChromaDB │ │   LLM    │
                    └──────────┘ └──────────┘
                            │
                            ↓
                    Relevant Sources
```

## 🔄 RAG Pipeline

### 1. Document Ingestion

Uploaded documents are extracted into text.

Supported formats:

* PDF
* DOCX
* TXT

### 2. Chunking

Documents are divided into smaller pieces using a recursive text splitter.

This allows the retrieval system to search for relevant sections rather than passing entire documents to the LLM.

### 3. Embeddings

Each chunk is converted into a numerical vector using:

```text
all-MiniLM-L6-v2
```

The same embedding model is used for both documents and user questions.

### 4. Vector Storage

Embeddings and metadata are stored in ChromaDB.

Metadata includes information such as:

* document ID
* filename
* page
* chunk ID

### 5. Retrieval

When a user asks a question:

```text
Question
   ↓
Question Embedding
   ↓
Semantic Similarity Search
   ↓
Relevant Chunks
```

### 6. Generation

Retrieved chunks are inserted into a grounded prompt and passed to the LLM.

The model is instructed to answer using only the retrieved context and avoid inventing information.

### 7. Source Attribution

The API returns the answer together with source information so users can identify which document and page provided the relevant context.

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* Pydantic
* SQLModel
* SQLite

### RAG / AI

* LangChain
* Sentence Transformers
* ChromaDB
* Google Gemini

### Document Processing

* PyPDF
* python-docx

### Frontend

* HTML
* CSS
* JavaScript

### Testing

* pytest

## 📁 Project Structure

```text
smart-knowledge-assistant/
│
├── backend/
│   ├── api/
│   ├── evaluation/
│   ├── models/
│   ├── rag/
│   ├── services/
│   ├── data/
│   ├── database.py
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── tests/
│
├── .env.example
├── .gitignore
└── README.md
```

## 🚀 Running the Project

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd smart-knowledge-assistant
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r backend/requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```text
GOOGLE_API_KEY=your_google_api_key_here
```

### 5. Start the backend

From the project root:

```powershell
uvicorn backend.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the frontend

Open another terminal:

```powershell
cd frontend
python -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500
```

## 🧪 Running Tests

From the project root:

```powershell
pytest
```

## 📊 RAG Evaluation

The project includes a basic retrieval evaluation pipeline.

Run:

```powershell
python -m backend.evaluation.evaluate_retrieval
```

The evaluation measures whether the expected document and page appear among the retrieved results.

## 🔐 Security Notes

API keys are stored in environment variables and should never be committed to the repository.

Uploaded documents and local databases are excluded from Git through `.gitignore`.

## 🎯 Learning Goals

This project was built to understand the complete RAG pipeline rather than relying only on a pre-built abstraction.

Key concepts explored:

* Document ingestion
* Text extraction
* Chunking
* Embeddings
* Vector databases
* Semantic search
* Retrieval
* Prompt construction
* Context injection
* Grounded generation
* Source attribution
* RAG evaluation
* FastAPI API development
* Frontend/backend integration

## 🔮 Future Improvements

Potential future improvements include:

* Hybrid search
* Reranking
* Metadata filtering
* Context compression
* Streaming responses
* Background document processing
* Improved evaluation datasets
* Authentication
* Conversation history
* Production deployment

## 📄 License

MIT License
