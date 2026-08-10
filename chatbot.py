import csv
from pathlib import Path
from typing import List, Tuple

FAQ_FILE = Path(__file__).with_name("faq.csv")


def load_faq(file_path: Path | None = None) -> List[Tuple[str, str]]:
    """Load FAQ entries from the CSV file, or fall back to sample data."""
    path = file_path or FAQ_FILE

    if path.exists():
        with path.open("r", encoding="utf-8", newline="") as file:
            rows = list(csv.reader(file))

        faq = []
        for row in rows:
            if len(row) >= 2:
                question = row[0].strip()
                answer = row[1].strip()
                if question and answer:
                    faq.append((question, answer))
        if faq:
            return faq

    return [
        ("What is this chatbot about?", "This is an AI-powered FAQ assistant built with Streamlit."),
        ("How does it work?", "It reads your question and matches it against a set of FAQ entries to provide a helpful answer."),
        ("Can I customize the answers?", "Yes. You can update the FAQ data in the FAQ CSV file to fit your project."),
        ("Is this project beginner-friendly?", "Absolutely. The app is designed to be simple, clean, and easy to extend."),
    ]


def get_answer(question: str, faq: List[Tuple[str, str]] | None = None) -> str:
    """Return the best matching FAQ answer for a user question."""
    if not question or not question.strip():
        return "Please enter a question so I can help you."

    if faq is None:
        faq = load_faq()

    normalized_question = question.strip().lower()

    for faq_question, answer in faq:
        normalized_faq = faq_question.lower()
        if normalized_question in normalized_faq or normalized_faq in normalized_question:
            return answer

    return "I couldn't find a matching answer yet. Please try another question or ask the developer to add it."

