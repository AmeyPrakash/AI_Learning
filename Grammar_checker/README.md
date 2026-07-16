# Grammar Checker

A command-line tool that leverages the Groq API and LLaMA 3.3 70B model to check and improve English grammar and writing quality.

## Overview

This Grammar Checker uses the Groq API to analyze your text and provide professional grammar corrections while preserving the original meaning and tone. It's designed to help improve writing quality through automated grammar, spelling, punctuation, and sentence structure enhancement.

## Features

- ✅ Grammar and spelling corrections
- ✅ Punctuation and capitalization fixes
- ✅ Sentence structure improvement
- ✅ Preserves original meaning and intent
- ✅ No additional comments or explanations added
- ✅ Interactive command-line interface

## Requirements

- Python >= 3.14
- Groq API key
- groq library
- python-dotenv library

## Setup

### 1. Install Dependencies

```bash
pip install groq python-dotenv
```

### 2. Configure API Key

Create a `.env` file in the parent directory (`AI_Learning/`) with your Groq API key:

```
GROQ_API_KEY=your_api_key_here
```

**Note:** The script looks for the `.env` file at `AI_Learning/.env` using:
```python
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
```

### 3. Run the Script

```bash
python grammar_checker.py
```

## Usage

1. Run the script
2. Enter your text, line by line
3. Press Enter twice when finished (empty line)
4. The improved text will be displayed

### Example

```
Enter your text (Press Enter twice to finish):
i is here and i need too learn pyton programing
its very difficul but im enjoying it


i is here and I need to learn Python programming. It's very difficult, but I'm enjoying it.
```

## How It Works

- Uses the **LLaMA 3.3 70B Versatile** model via Groq API
- Acts as a professional English grammar and writing assistant
- Processes your input through the system and user prompts
- Returns only the corrected text without additional commentary

## Model Details

- **Model:** llama-3.3-70b-versatile
- **Provider:** Groq API

## Configuration

The tool is configured with the following system prompt:
- Correct grammar, spelling, punctuation, and capitalization
- Improve sentence structure and readability
- Preserve original meaning and intent
- Return ONLY the improved text (no explanations or comments)