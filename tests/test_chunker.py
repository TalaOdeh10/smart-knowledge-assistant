from backend.rag.chunker import split_text


def test_split_text():

    text = "one two three four five six seven eight"

    chunks = split_text(
        text,
        chunk_size=15,
        chunk_overlap=3,
    )

    assert len(chunks) > 1