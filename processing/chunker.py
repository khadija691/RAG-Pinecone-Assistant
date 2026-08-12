def chunk_pages(
    pages: list[dict],
    chunk_size: int = 500,
    overlap: int = 50
) -> list[dict]:
    """
    Split extracted PDF pages into overlapping chunks
    while preserving page numbers.
    """

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []

    for page_data in pages:

        page_number = page_data["page"]
        text = page_data["text"]

        if not text:
            continue

        start = 0
        chunk_number = 0

        while start < len(text):

            end = start + chunk_size

            chunk = text[start:end].strip()

            if chunk:
                chunks.append({
                    "id": f"page{page_number}-chunk{chunk_number}",
                    "page": page_number,
                    "text": chunk
                })

                chunk_number += 1

            if end >= len(text):
                break

            start = end - overlap

    return chunks