import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


# ==========================================
# AZURE OPENAI CLIENT
# ==========================================

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT")
)


# This must match your Azure deployment name
AZURE_DEPLOYMENT = os.getenv(
    "AZURE_OPENAI_DEPLOYMENT"
)


FALLBACK_MESSAGE = (
    "The answer is not available in the provided document."
)


def generate_answer(
    query: str,
    retrieved_chunks: list[dict]
) -> str:
    """
    Generate an answer using only the retrieved PDF context.
    """

    if not retrieved_chunks:
        return FALLBACK_MESSAGE


    # ==========================================
    # BUILD CONTEXT
    # ==========================================

    context_parts = []

    for chunk in retrieved_chunks:

        context_parts.append(
            f"""
Document: {chunk['document']}
Page: {chunk['page']}
Similarity Score: {chunk['score']}

Content:
{chunk['text']}
"""
        )


    context = "\n".join(context_parts)


    # ==========================================
    # SYSTEM PROMPT
    # ==========================================

    system_prompt = """
You are a document question-answering assistant.

You MUST answer using ONLY the provided document context.

Rules:

1. Do not use outside knowledge.
2. Do not invent information.
3. If the answer cannot be found in the context, respond exactly:
   "The answer is not available in the provided document."
4. Keep the answer clear and concise.
5. Do not mention information that is not supported by the context.
"""


    # ==========================================
    # USER PROMPT
    # ==========================================

    user_prompt = f"""
Document Context:

{context}

Question:
{query}

Answer the question using only the document context.
"""


    # ==========================================
    # AZURE GPT REQUEST
    # ==========================================

    response = client.chat.completions.create(

        model=AZURE_DEPLOYMENT,

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],

       max_completion_tokens=300
    )


    return response.choices[0].message.content.strip()