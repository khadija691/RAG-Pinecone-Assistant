import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

print("===== AZURE OPENAI TEST =====")
print("API key loaded:", bool(api_key))
print("Endpoint:", endpoint)
print("Deployment:", deployment)

client = OpenAI(
    api_key=api_key,
    base_url=endpoint.rstrip("/") + "/"
)

print("\nSending test request...")

response = client.chat.completions.create(
    model=deployment,
    messages=[
        {
            "role": "user",
            "content": "Explain what a vector database is in one sentence."
        }
    ],
    max_completion_tokens=100
)

print("\n===== AZURE RESPONSE =====")
print(response.choices[0].message.content)

print("\n===== TEST SUCCESSFUL =====")