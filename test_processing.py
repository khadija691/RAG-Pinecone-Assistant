from loaders.pdf_loader import extract_pdf_pages
from processing.cleaner import clean_text
from processing.chunker import chunk_pages


PDF_PATH = "test.pdf"


# 1. Extract PDF
pages = extract_pdf_pages(PDF_PATH)

print("\n===== EXTRACTED PAGES =====")

for page in pages:

    print(
        f"\nPage {page['page']}:"
    )

    print(
        page["text"][:300]
    )


# 2. Clean text
for page in pages:

    page["text"] = clean_text(
        page["text"]
    )


# 3. Create chunks
chunks = chunk_pages(
    pages,
    chunk_size=500,
    overlap=50
)

print("\n===== CHUNKS =====")
print("Total chunks:", len(chunks))

for chunk in chunks:
    print("\n---")
    print("ID:", chunk["id"])
    print("Page:", chunk["page"])
    print("Text:", chunk["text"])