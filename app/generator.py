from google import genai
from google.genai import types

from .config import ANSWER_MODEL

client = genai.Client()


def build_context(passages: list[dict]) -> str:
    blocks = []

    for index, passage in enumerate(passages, start=1):
        blocks.append(
            f"[{index}] Source: {passage['source_name']} "
            f"(page {passage.get('page', 'N/A')})\n"
            f"{passage['text']}"
        )

    return "\n\n".join(blocks)


def generate_answer(question: str, passages: list[dict], temperature: float = 0.2):
    context = build_context(passages)

    prompt = f"""Answer the user question using only the context below.

Context:
{context}

Question:
{question}

Rules:
- If the context does not contain enough information, say that clearly.
- Cite every factual claim using bracketed numbers such as [1] or [2].
- Do not invent sources or facts.

Answer:"""

    response = client.models.generate_content(
        model=ANSWER_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=1024,
        ),
    )

    return response.text