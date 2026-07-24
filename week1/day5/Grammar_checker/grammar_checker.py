import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent


def load_project_env() -> None:
    for directory in (BASE_DIR, *BASE_DIR.parents):
        env_path = directory / ".env"
        if env_path.exists():
            load_dotenv(env_path)
            return


load_project_env()

model = "llama-3.3-70b-versatile"
role = "user"

# BEHAVIOR
system_prompt = """
You are a professional English grammar and writing assistant.

Your task is to improve the user's writing while preserving its original meaning and tone.

Instructions:
- Correct grammar, spelling, punctuation, and capitalization.
- Improve sentence structure and readability.
- Preserve the original meaning and intent.
- Do not add or remove information unless necessary for grammatical correctness.
- Do not explain your changes.
- Do not include comments, notes, or formatting.
- If the text is already correct, return it unchanged.
- Return ONLY the improved text.
"""

def get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "Groq API key not found. Add GROQ_API_KEY=your_key_here to a .env file in this project or one of its parent folders."
        )

    return Groq(api_key=api_key)


def read_user_text() -> str:
    print("Enter your text (Press Enter twice to finish):")
    lines = []

    while True:
        line = input()
        if not line:
            break

        lines.append(line)

    return "\n".join(lines)


def improve_text(text: str) -> str:
    user_prompt = f"""
Improve the grammar and readability of the following text while preserving its original meaning.

Text:
{text}
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": role,
            "content": user_prompt,
        },
    ]

    response = get_groq_client().chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content


def main() -> None:
    text = read_user_text()
    print(improve_text(text))


if __name__ == "__main__":
    main()
