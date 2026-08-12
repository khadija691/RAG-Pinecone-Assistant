from retrieval.retriever import retrieve


query = "What is this PDF about?"


print("===== QUERY =====")
print(query)


print("\n===== RETRIEVED RESULTS =====")

results = retrieve(
    query,
    top_k=3,
    score_threshold=0.40
)


for result in results:

    print("\n---")

    print("ID:", result["id"])
    print("Score:", result["score"])
    print("Page:", result["page"])
    print("Document:", result["document"])

    print("Text:")
    print(result["text"])