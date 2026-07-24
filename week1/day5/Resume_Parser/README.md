# Resume Parser

This project extracts text from a resume file and sends it to an AI model to evaluate how well the resume matches a job description.

It currently supports:

- PDF resumes using `pymupdf`
- Word `.docx` resumes using `python-docx`
- AI evaluation using Groq
- Structured JSON validation using Pydantic

## Project Flow

The main file is:

```text
resume_parser.py
```

The flow is:

```text
resume file -> text extraction -> prompt creation -> Groq API call -> JSON response -> Pydantic validation -> print result
```

## Important Concepts Used

### 1. `Path` From `pathlib`

The project uses `Path` instead of plain strings for file paths.

```python
BASE_DIR = Path(__file__).resolve().parent
```

This gives the folder where `resume_parser.py` exists.

Then resume files are loaded like this:

```python
resume_path = BASE_DIR / "resumes" / "resume.pdf"
```

This is better than:

```python
Path("resumes") / "resume.pdf"
```

because `Path("resumes")` depends on where the terminal is opened from. `BASE_DIR` makes the path reliable.

### 2. Extracting Text From PDF

PDF files are handled by `pymupdf`.

```python
def extract_pdf(pdf_path: Path) -> str:
    with pymupdf.open(pdf_path) as doc:
        return "\n".join(page.get_text() for page in doc)
```

This opens the PDF, loops through every page, extracts text, and joins all pages into one string.

### 3. Extracting Text From Word Documents

Word `.docx` files are handled by `python-docx`.

```python
def extract_docx(docx_path: Path) -> str:
    document = Document(docx_path)

    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    )
```

This reads all paragraphs and skips empty ones.

### 4. Dictionary-Based Function Dispatch

The project uses a dictionary to choose the correct extraction function.

```python
extractors = {
    ".pdf": extract_pdf,
    ".docx": extract_docx,
}
```

Then the file extension is checked:

```python
suffix = resume_path.suffix.lower()
extractor = extractors.get(suffix)
```

If the file is a PDF, `extract_pdf` runs.

If the file is a DOCX, `extract_docx` runs.

This avoids writing many `if/elif` statements.

### 5. `suffix.lower()`

The code uses:

```python
resume_path.suffix.lower()
```

This means file extensions are treated consistently.

Examples:

```text
resume.PDF  -> .pdf
resume.Docx -> .docx
```

### 6. Error Handling

The project checks if files exist before trying to read them.

```python
if not resume_path.exists():
    raise FileNotFoundError(f"File not found: {resume_path}")
```

It also rejects unsupported file types:

```python
if extractor is None:
    raise ValueError(f"Unsupported file type: {suffix}")
```

### 7. Environment Variables

The Groq API key is loaded from the first `.env` file found while walking upward from the `Resume_Parser` folder.

```python
load_project_env()
my_api_key = os.getenv("GROQ_API_KEY")
```

The `.env` file should contain:

```text
GROQ_API_KEY=your_api_key_here
```

This keeps secret keys out of the code.

### 8. Groq Client

The project creates a Groq client:

```python
client = Groq(api_key=my_api_key)
```

Then it sends messages to the model:

```python
response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format=response_format,
)
```

The `messages` list contains:

- a `system` message that tells the AI how to behave
- a `user` message that contains the job description and resume text

### 9. System Prompt vs User Prompt

The system prompt defines the AI's role and rules.

Example:

```text
You are an experienced Technical HR Recruiter and ATS.
Return ONLY valid JSON.
```

The user prompt contains the actual task data:

- job description
- candidate resume text
- evaluation rules

### 10. Pydantic Model

The AI is asked to return JSON. Pydantic checks that the JSON has the expected structure.

```python
class ResumeEvaluation(BaseModel):
    candidate_name: str
    job_title: str
    match_percentage: int
    overall_verdict: str
    summary: str
    matching_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    weaknesses: list[str]
    experience_match: str
    education_match: str
    project_match: str
    keyword_match_score: int
    recommendation: str
    interview_recommendation: str
    reasoning: str
```

Then the AI response is validated:

```python
return ResumeEvaluation.model_validate_json(answer)
```

This helps catch invalid or unexpected AI output.

### 11. Why `main()` Is Used

The project uses:

```python
def main() -> None:
    resume_path = BASE_DIR / "resumes" / "resume.pdf"
    evaluation = evaluate_resume(resume_path)
    print(evaluation.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
```

This means the script only runs when executed directly:

```bash
python resume_parser.py
```

If another Python file imports a function from this file, the full resume evaluation will not run automatically.

This makes the code reusable and safer.

## Current File Support

Supported extensions:

```text
.pdf
.docx
```

Unsupported files will raise:

```text
ValueError: Unsupported file type
```

## How To Run

From the `Resume_Parser` folder:

```bash
python resume_parser.py
```

Or from the parent folder:

```bash
python week1/day5/Resume_Parser/resume_parser.py
```

Both work because paths are based on `BASE_DIR`.

## Things To Improve Later

- Let the user pass the resume path from the command line.
- Move the job description into a separate `.txt` file.
- Add support for multiple resumes.
- Save the AI result to a JSON file.
- Add tests for PDF, DOCX, and unsupported file types.
- Add stricter validation for `match_percentage` so it must be between 0 and 100.
