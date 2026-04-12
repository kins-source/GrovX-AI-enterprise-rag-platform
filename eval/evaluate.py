import json
import os
import sys

# Add parent to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.orchestrator import process_query

def evaluate():
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset.json")
    with open(dataset_path, "r") as f:
        data = json.load(f)

    correct = 0
    total = len(data)

    print("Starting Evaluation Pipeline...\n")
    for item in data:
        q = item["question"]
        keywords = item["expected_answer_keywords"]
        
        print(f"Q: {q}")
        res = process_query(q)
        answer = res["answer"].lower()
        
        # Simple heuristic: check if at least one keyword is present
        passed = any(kw.lower() in answer for kw in keywords)
        
        if passed:
            correct += 1
            print("[PASS]")
        else:
            print("[FAIL]")
        print(f"Actual Answer: {res['answer']}\n")

    accuracy = (correct / total) * 100
    print(f"=== Evaluation Complete ===")
    print(f"Accuracy: {accuracy:.2f}% ({correct}/{total})")

if __name__ == "__main__":
    evaluate()
