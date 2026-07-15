# Day 4

This folder contains a simple Day 4 learning project focused on Python basics and a small AI-powered example using Groq and Pydantic.

## Files

- main.py: a basic script that prints a simple message.
- jason_pydantic.py: demonstrates loading environment variables, calling the Groq API, and validating extracted information using Pydantic.
- pyproject.toml: project configuration and dependencies.

## Dependencies

The project uses:

- groq
- pydantic
- python-dotenv

## Run

To run the basic example:

```bash
python main.py
```

To run the Pydantic/Groq example:

```bash
python jason_pydantic.py
```

Make sure your environment variable `GROQ_API_KEY` is set before running the API example.
