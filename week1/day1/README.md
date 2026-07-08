# Groq API Chat Completion (Python)

A simple Python program that uses the **Groq API** to generate text using the **Llama 3.3 70B Versatile** model.

## Concepts Used

- Python
- Environment Variables (`.env`)
- `python-dotenv`
- Groq Python SDK
- Chat Completions API

## What This Program Does

- Loads the Groq API key from a `.env` file.
- Creates a Groq client.
- Sends a prompt to the Llama 3.3 model.
- Prints the complete API response.
- Extracts and displays only the generated answer.

## Setup

1. Install the required packages:

```bash
pip install groq python-dotenv
```

2. Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_api_key_here
```

3. Run the script:

```bash
python main.py
```

## Example Prompt

```text
Write a short poem about the beauty of nature.
```

## Output

The program prints:
- The complete API response
- The generated text from the AI model