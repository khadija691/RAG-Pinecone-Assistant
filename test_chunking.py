from loaders.pdf_loader import extract_pdf_pages
from processing.cleaner import clean_text
from processing.chunker import chunk_pages


PDF_PATH = "test.pdf"


# Extract pages
pages = extract_pdf_pages(PDF_PATH)


# Clean text
for page in pages:
    page["text"] = clean_text(page["text"])
    page["document"] = PDF_PATH


# Create chunks
chunks = chunk_pages(
    pages,
    chunk_size=500,
    overlap=50
)


print("\n===== CHUNKS =====")
print("Total chunks:", len(chunks))

for chunk in chunks:

    print("\n--------------------")

    print("ID:", chunk["id"])
    print("Page:", chunk["page"])
    print("Document:", chunk["document"])
    print("Text:", chunk["text"])