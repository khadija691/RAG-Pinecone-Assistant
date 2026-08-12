from flask import Flask, render_template, request, jsonify
import tempfile
import os

from loaders.pdf_loader import extract_pdf_pages
from processing.cleaner import clean_text
from processing.chunker import chunk_pages
from embeddings.embedder import generate_embeddings
from vectorstore.pinecone_store import create_index, get_index
from retrieval.retriever import retrieve
from generation.generator import generate_answer


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "pdf" not in request.files:
        return jsonify({
            "error": "No PDF uploaded"
        }), 400

    pdf = request.files["pdf"]

    if pdf.filename == "":
        return jsonify({
            "error": "No PDF selected"
        }), 400

    # Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        pdf.save(temp_file.name)
        pdf_path = temp_file.name

    try:

        # ==========================================
        # STEP 1: PDF EXTRACTION
        # ==========================================

        pages = extract_pdf_pages(pdf_path)

        # ==========================================
        # STEP 2: CLEANING
        # ==========================================

        cleaned_pages = []

        for page in pages:
            cleaned_pages.append({
                "page": page["page"],
                "text": clean_text(page["text"])
            })

        # ==========================================
        # STEP 3: CHUNKING
        # ==========================================

        chunks = chunk_pages(cleaned_pages)

        # ==========================================
        # STEP 4: EMBEDDINGS
        # ==========================================

        embedded_chunks = generate_embeddings(chunks)

        # ==========================================
        # STEP 5: PINECONE
        # ==========================================

        create_index()
        index = get_index()

        vectors = []

        for item in embedded_chunks:

            vectors.append({
                "id": item["id"],
                "values": item["embedding"],
                "metadata": {
                    "page": item["page"],
                    "document": pdf.filename,
                    "chunk_id": item["id"],
                    "text": item["text"]
                }
            })

        # Upload vectors
        index.upsert(vectors=vectors)

        return jsonify({
            "success": True,
            "filename": pdf.filename,
            "pages": len(pages),
            "chunks": len(chunks),
            "message": "PDF processed and stored successfully."
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:

        # Delete temporary PDF
        if os.path.exists(pdf_path):
            os.remove(pdf_path)


@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({
            "error": "No question provided"
        }), 400

    question = data["question"].strip()

    if not question:
        return jsonify({
            "error": "Question cannot be empty"
        }), 400

    try:

        # ==========================================
        # STEP 1: RETRIEVAL
        # ==========================================

        retrieved_chunks = retrieve(question)

        # ==========================================
        # STEP 2: AZURE GPT GENERATION
        # ==========================================

        answer = generate_answer(
            question,
            retrieved_chunks
        )

        # ==========================================
        # STEP 3: SOURCES
        # ==========================================

        sources = []

        for chunk in retrieved_chunks:

            sources.append({
                "page": chunk["page"],
                "score": chunk["score"],
                "document": chunk["document"]
            })

        return jsonify({
            "success": True,
            "answer": answer,
            "sources": sources
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)