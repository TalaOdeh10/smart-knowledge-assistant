from backend.rag.loader import load_document


def test_load_txt():

    pages = load_document(
        "backend/data/documents/company_policy.txt"
    )

    assert len(pages) > 0

    assert "remote" in pages[0]["text"].lower()