# Groq API - System & User Roles

A simple Python program demonstrating how to use **System** and **User** roles with the **Groq Chat Completions API**.

## Concepts Used

- Python
- Environment Variables (`.env`)
- `python-dotenv`
- Groq Python SDK
- Chat Completions API
- System Role
- User Role
- Temperature Parameter

## What This Program Does

- Loads the Groq API key from a `.env` file.
- Creates a Groq client.
- Sets a **System** role to define the AI's behavior.
- Sends a **User** prompt asking for a poem.
- Uses `temperature=0` for a more consistent response.
- Prints the AI-generated poem.

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

## Example

**System Prompt**

```text
You are a wise and old poet who writes poems about nature and the environment.
```

**User Prompt**

```text
Write a poem about a river and a sea.
```

## Output

The program generates a poem that follows the personality defined by the **System** role.