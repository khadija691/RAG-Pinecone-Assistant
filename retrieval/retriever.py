from embeddings.embedder import model
from vectorstore.pinecone_store import get_index


def retrieve(
    query: str,
    top_k: int = 3,
    score_threshold: float = 0.30
) -> list[dict]:
    """
    Retrieve the most relevant chunks from Pinecone.

    Broad questions use a lower threshold because they may
    require several general document sections.
    """

    if not query or not query.strip():
        return []

    query = query.strip()

    # Broad/general questions need more context
    broad_keywords = [
         "what is this",
    "what's this",
    "what is the pdf",
    "what's the pdf",
    "what is this pdf",
    "what is this document",
    "what is the document",
    "summarize",
    "summary",
    "summarise",
    "overview",
    "explain this pdf",
    "explain the pdf",
    "explain this document",
    "explain the document",
    "explain the content",
    "content of this pdf",
    "content of the pdf",
    "content of this document",
    "content of the document",
    "what is the content",
    "what does this document",
    "what does the document",
    "what does this pdf",
    "what does the pdf",
    "tell me about this document",
    "tell me about the document",
    "tell me about this pdf",
    "tell me about the pdf",
    "main points",
    "main topics",
    "key points",
    "give me a summary",
    "give me an overview",
    "how many images are there",
    "explain the content of the images in the pdf",
    "how to fill this pdf",
    "advantages and disadvantages of the content in the pdf",

    ]

    is_broad_question = any(
        keyword in query.lower()
        for keyword in broad_keywords
    )

    if is_broad_question:
        top_k = 10
        score_threshold = 0.15
    else:
        top_k = 3
        score_threshold = 0.35

    # Create query embedding
    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    # Get Pinecone index
    index = get_index()

    # Search Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    retrieved_chunks = []

    for match in results["matches"]:

        score = match["score"]

        # Ignore weak matches
        if score < score_threshold:
            continue

        metadata = match["metadata"]

        retrieved_chunks.append({
            "id": match["id"],
            "score": score,
            "page": metadata.get("page"),
            "document": metadata.get("document"),
            "chunk_id": metadata.get("chunk_id"),
            "text": metadata.get("text", "")
        })

    return retrieved_chunks