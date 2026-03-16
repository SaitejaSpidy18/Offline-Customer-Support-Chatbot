import json
from pathlib import Path

import requests

# ==== Constants ====
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"  # Ollama REST API endpoint[web:1][web:17]
MODEL_NAME = "llama3.2:3b"

PROJECT_ROOT = Path(__file__).parent
PROMPTS_DIR = PROJECT_ROOT / "prompts"
EVAL_DIR = PROJECT_ROOT / "eval"
RESULTS_FILE = EVAL_DIR / "results.md"


# ==== Customer queries (20 adapted e-commerce queries) ====
CUSTOMER_QUERIES = [
    "How do I track the shipping status of my recent order?",
    "My discount code is not working at checkout, what should I do?",
    "I received a damaged item, how can I request a replacement?",
    "Can I change the delivery address after placing my order?",
    "What payment methods do you accept on Chic Boutique?",
    "I was charged twice for my order, how can I get a refund?",
    "How do I cancel an order that has not been shipped yet?",
    "The size I ordered does not fit, how can I exchange it?",
    "Do you offer international shipping and how long does it take?",
    "I never received the order confirmation email, what should I check?",
    "An item is showing as out of stock, will it be restocked soon?",
    "How do I apply a gift card to my purchase?",
    "My package says delivered but I have not received it, what can I do?",
    "Can I return sale or discounted items?",
    "How do I update my saved payment information in my account?",
    "I entered the wrong email address during checkout, can you fix it?",
    "Do you offer cash-on-delivery or pay-on-delivery options?",
    "How can I subscribe or unsubscribe from your marketing emails?",
    "Is it possible to combine two orders into one shipment?",
    "How do I contact support if I have an issue with my order?",
]


# ==== Helpers ====
def query_ollama(prompt: str) -> str:
    """
    Send a prompt to the local Ollama server using /api/generate
    and return the model's response text.
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,  # full response in one go[web:13][web:14]
    }

    try:
        response = requests.post(OLLAMA_ENDPOINT, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()
    except requests.exceptions.RequestException as e:
        print(f"Error querying Ollama: {e}")
        return "Error: Could not get a response from the model."


def load_template(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def init_results_file() -> None:
    """
    Initialize eval/results.md with a rubric description and table header.
    """
    header = """## Scoring Rubric

- Relevance (1–5): How well does the response address the customer's query?
- Coherence (1–5): Is the response grammatically correct and easy to understand?
- Helpfulness (1–5): Does the response provide clear, actionable guidance?

(1 = very poor, 5 = excellent)

| Query # | Customer Query | Prompting Method | Response | Relevance (1-5) | Coherence (1-5) | Helpfulness (1-5) |
|--------:|----------------|------------------|----------|------------------|------------------|--------------------|
"""
    RESULTS_FILE.write_text(header, encoding="utf-8")


def append_result_row(query_idx: int, customer_query: str, method: str, response: str) -> None:
    """
    Append one row to the markdown table in eval/results.md.
    Scores are left blank for manual filling.
    """
    safe_query = customer_query.replace("|", "\\|")
    safe_response = response.replace("|", "\\|").replace("\n", " ")

    row = f"| {query_idx} | {safe_query} | {method} | {safe_response} |  |  |  |\n"

    with RESULTS_FILE.open("a", encoding="utf-8") as f:
        f.write(row)


def main() -> None:
    # Ensure eval directory exists
    EVAL_DIR.mkdir(parents=True, exist_ok=True)

    # Load templates
    zero_shot_template = load_template(PROMPTS_DIR / "zero_shot_template.txt")
    one_shot_template = load_template(PROMPTS_DIR / "one_shot_template.txt")

    # Initialize results file
    init_results_file()

    # Loop through all queries
    for idx, customer_query in enumerate(CUSTOMER_QUERIES, start=1):
        print(f"Processing query {idx}/20...")

        # Zero-shot
        zero_prompt = zero_shot_template.format(query=customer_query)
        zero_response = query_ollama(zero_prompt)
        append_result_row(idx, customer_query, "Zero-Shot", zero_response)

        # One-shot
        one_prompt = one_shot_template.format(query=customer_query)
        one_response = query_ollama(one_prompt)
        append_result_row(idx, customer_query, "One-Shot", one_response)

    print("Done. Check eval/results.md for outputs.")


if __name__ == "__main__":
    main()
