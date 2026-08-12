from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embeddings(chunks: list[dict]) -> list[dict]:
    """
    Generate embeddings for page-aware chunks.

    Each returned item keeps the original chunk information
    and adds a 384-dimensional embedding.
    """

    if not chunks:
        return []

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    results = []

    for chunk, embedding in zip(chunks, embeddings):

        results.append({
            "id": chunk["id"],
            "page": chunk["page"],
            "text": chunk["text"],
            "embedding": embedding.tolist()
        })

    return results