from backend.rag.pipeline import retrieve_context
from backend.evaluation.questions import TEST_QUESTIONS


def evaluate():

    correct = 0

    for item in TEST_QUESTIONS:

        results = retrieve_context(
            item["question"],
            top_k=3,
        )

        metadatas = results["metadatas"][0]

        found = any(
            metadata["source"] == item["expected_source"]
            and metadata["page"] == item["expected_page"]
            for metadata in metadatas
        )

        if found:
            correct += 1

        print(
            f"{item['question']} → "
            f"{'PASS' if found else 'FAIL'}"
        )

    score = correct / len(TEST_QUESTIONS)

    print()
    print(f"Retrieval Recall@3: {score:.2%}")


if __name__ == "__main__":
    evaluate()