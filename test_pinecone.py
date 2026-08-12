from loaders.pdf_loader import extract_pdf_pages
from processing.cleaner import clean_text
from processing.chunker import chunk_pages
from embeddings.embedder import generate_embeddings

from vectorstore.pinecone_store import (
    create_index,
    upsert_chunks,
    get_index
)


PDF_PATH = "test.pdf"
DOCUMENT_NAME = "test.pdf"


print("===== STEP 1: PDF EXTRACTION =====")

pages = extract_pdf_pages(PDF_PATH)

print("Pages:", len(pages))


print("\n===== STEP 2: CLEANING =====")

for page in pages:
    page["text"] = clean_text(page["text"])

print("Cleaning completed.")


print("\n===== STEP 3: CHUNKING =====")

chunks = chunk_pages(
    pages,
    chunk_size=500,
    overlap=50
)

print("Chunks:", len(chunks))


print("\n===== STEP 4: EMBEDDINGS =====")

embedded_chunks = generate_embeddings(chunks)

print(
    "Embeddings:",
    len(embedded_chunks)
)


print("\n===== STEP 5: PINECONE =====")

create_index()

upsert_chunks(
    embedded_chunks,
    DOCUMENT_NAME
)


print("\n===== STEP 6: TEST COMPLETE =====")

index = get_index()

print("Pinecone index connected successfully.")

print(index)