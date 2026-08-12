from processing.ocr import extract_ocr_from_pdf


PDF_PATH = "ocr_test.pdf"


pages = extract_ocr_from_pdf(PDF_PATH)


print("\n===== OCR RESULTS =====")

for page in pages:

    print("\n--------------------")
    print("Page:", page["page"])
    print("Text:")
    print(page["text"])