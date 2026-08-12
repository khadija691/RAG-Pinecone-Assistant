from retrieval.retriever import retrieve
from generation.generator import generate_answer


def test_question(query):

    print("\n" + "=" * 60)
    print("QUESTION:")
    print(query)

    print("\nRetrieving relevant context...")

    # Let retriever.py automatically choose
    # the appropriate top_k and threshold.
    results = retrieve(query)

    print(f"Retrieved chunks: {len(results)}")

    answer = generate_answer(
        query,
        results
    )

    print("\n===== AI ANSWER =====")
    print(answer)

    print("\n===== SOURCES =====")

    for result in results:
        print(
            f"Page {result['page']} | "
            f"Score: {result['score']:.3f}"
        )


# Question where the answer exists
test_question(
    "What is this PDF about?"
)


# Question where the answer should NOT exist
test_question(
    "What programming language did the student use to build a mobile application?"
)