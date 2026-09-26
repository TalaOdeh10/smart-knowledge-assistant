from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"#It produces vectors with:384 dimensions

model = SentenceTransformer(MODEL_NAME)

def create_embeddings(texts: list[str]):
    return model.encode(texts)