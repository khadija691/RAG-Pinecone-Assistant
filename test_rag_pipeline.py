from loaders.pdf_loader import extract_pdf_pages
from processing.cleaner import clean_text
from processing.chunker import chunk_pages

from embeddings.embedder import generate_embeddings

from vectorstore.pinecone_store import (
    create_index,
    upsert_chunks,
    query_chunks
)


PDF_PATH = "test.pdf"


print("===== STEP 1: PDF EXTRACTION =====")

pages = extract_pdf_pages(PDF_PATH)

for page in pages:
    page["text"] = clean_text(page["text"])
    page["document"] = PDF_PATH

print("Pages extracted:", len(pages))


print("\n===== STEP 2: CHUNKING =====")

chunks = chunk_pages(
    pages,
    chunk_size=500,
    overlap=50
)

print("Total chunks:", len(chunks))


print("\n===== STEP 3: EMBEDDINGS =====")

texts = [chunk["text"] for chunk in chunks]

embeddings = generate_embeddings(texts)

print("Generated embeddings:", len(embeddings))
print("Vector dimension:", len(embeddings[0]))


print("\n===== STEP 4: PINECONE =====")

create_index()

upsert_chunks(
    chunks,
    embeddings
)


print("\n===== STEP 5: TEST RETRIEVAL =====")

query = "What did the student learn during the internship?"

print("Query:", query)

query_embedding = generate_embeddings([query])[0]

results = query_chunks(
    query_embedding,
    top_k=3
)


print("\n===== RETRIEVED RESULTS =====")

for match in results["matches"]:

    print("\n--------------------")

    print("ID:", match["id"])
    print("Score:", match["score"])
    print("Page:", match["metadata"]["page"])
    print("Document:", match["metadata"]["document"])

    print("Text:")
    print(match["metadata"]["text"])