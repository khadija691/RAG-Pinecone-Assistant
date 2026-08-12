import pymupdf

from processing.ocr import extract_ocr_from_pdf


def extract_pdf_pages(pdf_path: str) -> list[dict]:
    """
    Extract text from a PDF.

    If a page contains normal selectable text, use that text.
    If the page is image/scanned based and has little/no text,
    use Tesseract OCR.
    """

    document = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):

        # Try normal PDF text extraction first
        text = page.get_text("text").strip()

        # If the page has little/no selectable text,
        # OCR will be used for the page.
        if len(text) < 20:

            print(f"Page {page_number}: little/no text found. Using OCR...")

            # Render page as an image
            pixmap = page.get_pixmap(
                matrix=pymupdf.Matrix(2, 2)
            )

            from PIL import Image
            import pytesseract

            image = Image.frombytes(
                "RGB",
                [pixmap.width, pixmap.height],
                pixmap.samples
            )

            text = pytesseract.image_to_string(
                image,
                lang="eng"
            ).strip()

        pages.append({
            "page": page_number,
            "text": text
        })

    document.close()

    return pages