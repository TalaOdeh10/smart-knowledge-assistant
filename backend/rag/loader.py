

from pathlib import Path

from pypdf import PdfReader
from docx import Document


def load_txt(file_path: str) -> list[dict]:
    path = Path(file_path)

    with open(path, "r", encoding="utf-8") as file:
        text = file.read()

    return [
        {
            "text": text,
            "page": 1,
        }
    ]


def load_pdf(file_path: str) -> list[dict]:
    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            pages.append(
                {
                    "text": text,
                    "page": page_number,
                }
            )

    return pages


def load_docx(file_path: str) -> list[dict]:
    document = Document(file_path)

    text = "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    )

    return [
        {
            "text": text,
            "page": 1,
        }
    ]


def load_document(file_path: str) -> list[dict]:
    extension = Path(file_path).suffix.lower()

    if extension == ".txt":
        return load_txt(file_path)

    if extension == ".pdf":
        return load_pdf(file_path)

    if extension == ".docx":
        return load_docx(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )