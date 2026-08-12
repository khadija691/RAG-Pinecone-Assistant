import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

INDEX_NAME = "rag-pinecone-assistant"
DIMENSION = 384

pc = Pinecone(api_key=PINECONE_API_KEY)


def create_index():

    existing_indexes = [index["name"] for index in pc.list_indexes()]

    if INDEX_NAME not in existing_indexes:

        pc.create_index(
            name=INDEX_NAME,
            dimension=DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

        print(f"Created Pinecone index: {INDEX_NAME}")

    else:

        print(f"Pinecone index already exists: {INDEX_NAME}")


def get_index():

    return pc.Index(INDEX_NAME)


def upsert_chunks(
    embedded_chunks: list[dict],
    document_name: str
):
    """
    Upload embedded chunks to Pinecone with metadata.
    """

    index = get_index()

    vectors = []

    for chunk in embedded_chunks:

        vectors.append({
            "id": chunk["id"],

            "values": chunk["embedding"],

            "metadata": {
                "page": chunk["page"],
                "document": document_name,
                "chunk_id": chunk["id"],
                "text": chunk["text"]
            }
        })

    if vectors:

        index.upsert(
            vectors=vectors
        )

        print(
            f"Upserted {len(vectors)} vectors into Pinecone."
        )