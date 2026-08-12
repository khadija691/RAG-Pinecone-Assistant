from loaders.pdf_loader import extract_pdf_pages
from processing.cleaner import clean_text
from processing.chunker import chunk_pages
from embeddings.embedder import generate_embeddings


PDF_PATH = "test.pdf"


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

print("Embeddings generated:", len(embedded_chunks))

if embedded_chunks:
    print(
        "Embedding dimension:",
        len(embedded_chunks[0]["embedding"])
    )

    print(
        "First chunk ID:",
        embedded_chunks[0]["id"]
    )

    print(
        "First chunk page:",
        embedded_chunks[0]["page"]
    )

    print(
        "First 5 values:",
        embedded_chunks[0]["embedding"][:5]
    )