import os
import pymupdf
import pytesseract
from PIL import Image


# Tesseract installation path on Windows
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def extract_ocr_from_pdf(pdf_path: str) -> list[dict]:
    """
    Extract text from images inside a PDF using Tesseract OCR.

    Returns:
        [
            {
                "page": page_number,
                "text": extracted_text
            }
        ]
    """

    document = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):

        # Render PDF page as an image
        pixmap = page.get_pixmap(matrix=pymupdf.Matrix(2, 2))

        image = Image.frombytes(
            "RGB",
            [pixmap.width, pixmap.height],
            pixmap.samples
        )

        # OCR the image
        text = pytesseract.image_to_string(
            image,
            lang="eng"
        )

        pages.append({
            "page": page_number,
            "text": text.strip()
        })

    document.close()

    return pages