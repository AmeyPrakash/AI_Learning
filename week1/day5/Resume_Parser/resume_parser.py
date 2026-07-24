import os
import sys
from pathlib import Path

try:
    import pymupdf
    from docx import Document
    from dotenv import load_dotenv
    from groq import APIConnectionError, Groq
    from pydantic import BaseModel, ValidationError
except ImportError as exc:
    missing_module = exc.name or "a required package"
    raise SystemExit(
        f"Missing dependency: {missing_module}. From the Resume_Parser folder, run "
        "`uv run python resume_parser.py` or `.\\.venv\\Scripts\\python.exe resume_parser.py`. "
        "Do not run it with a global Python installation unless you installed this project's dependencies there."
    ) from exc


BASE_DIR = Path(__file__).resolve().parent


def load_project_env() -> None:
    for directory in (BASE_DIR, *BASE_DIR.parents):
        env_path = directory / ".env"
        if env_path.exists():
            load_dotenv(env_path)
            return


load_project_env()

model = "llama-3.3-70b-versatile"

response_format = {
    "type": "json_object"
}


def get_groq_client() -> Groq:
    """Create the Groq client after environment variables are loaded."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "Groq API key not found. Add GROQ_API_KEY=your_key_here to a .env file in this project or one of its parent folders."
        )

    return Groq(api_key=api_key)

# data we will need as output
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

#extracting PDF data using pymupdf
def extract_pdf(pdf_path: Path) -> str:
    """Extract all text from a PDF."""

    if not pdf_path.exists():
        raise FileNotFoundError(f"File not found: {pdf_path}")

    with pymupdf.open(pdf_path) as doc:
        return "\n".join(page.get_text() for page in doc)

#extracting word data using docx
def extract_docx(docx_path: Path) -> str:
    """Extract text from a Word (.docx) resume."""

    if not docx_path.is_file():
        raise FileNotFoundError(f"No document found at: {docx_path}")

    document = Document(docx_path)

    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    )

#types of the format for resume 
extractors = {
    ".pdf": extract_pdf,
    ".docx": extract_docx,
}

#determining the type of file for extraction whether pdf or docx
def extract_resume_text(resume_path: Path) -> str:
    """Extract resume text based on the file extension."""

    if not resume_path.exists():
        raise FileNotFoundError(f"File not found: {resume_path}")

    suffix = resume_path.suffix.lower()
    extractor = extractors.get(suffix)

    if extractor is None:
        raise ValueError(f"Unsupported file type: {suffix}")

    return extractor(resume_path)


job_description = """
Job Title: Frontend Developer Intern

Required Skills

HTML
CSS
JavaScript
TypeScript
React.js
Tailwind CSS
Git
REST APIs
Responsive Design
Figma

Preferred Skills

Next.js
Redux
Node.js
Firebase
Vercel

"""

system_prompt = """You are an experienced Technical HR Recruiter and ATS (Applicant Tracking System).

Your task is to evaluate a candidate's resume against a given job description.

Instructions:

1. Carefully analyze both the resume and the job description.
2. Compare:
   - Technical skills
   - Programming languages
   - Frameworks
   - Libraries
   - Tools
   - Education
   - Certifications
   - Experience
   - Projects
   - Soft skills
   - Keywords
   - Responsibilities
3. Determine how well the candidate matches the job requirements.
4. Do not invent information that is not present in the resume.
5. If information is missing, mention it as "Not Mentioned".
6. Base the score only on the information provided.
7. The match percentage must be an integer between 0 and 100.
8. Return ONLY valid JSON.
9. Do not include markdown, explanations, or code fences.

Return JSON in exactly this format:

{
  "candidate_name": "",
  "job_title": "",
  "match_percentage": 0,
  "overall_verdict": "",
  "summary": "",
  "matching_skills": [],
  "missing_skills": [],
  "strengths": [],
  "weaknesses": [],
  "experience_match": "",
  "education_match": "",
  "project_match": "",
  "keyword_match_score": 0,
  "recommendation": "",
  "interview_recommendation": "",
  "reasoning": ""
}

Scoring Guidelines:

90-100:
Excellent fit. Candidate satisfies nearly all required qualifications.

75-89:
Strong fit. Candidate satisfies most important requirements with minor gaps.

60-74:
Moderate fit. Candidate has several matching skills but noticeable gaps.

40-59:
Weak fit. Candidate lacks many important requirements.

0-39:
Poor fit. Candidate does not meet the primary requirements.

The response must always be valid JSON."""


def build_user_prompt(resume_text: str) -> str:
    return f"""
You are provided with:

1. A Job Description
2. A Candidate Resume

Your task is to compare them and determine how well the candidate fits the role.

Job Description
================
{job_description}

Candidate Resume
================
{resume_text}

Evaluation Criteria:
- Technical Skills
- Programming Languages
- Frameworks & Libraries
- Databases
- Cloud Technologies
- Tools
- Experience
- Education
- Projects
- Certifications
- Soft Skills
- Keyword Matching

Important Rules:
- Only use information explicitly mentioned in the resume.
- Do not hallucinate experience or skills.
- Mention missing required skills.
- Explain why the candidate received the final score.
- Return ONLY valid JSON as defined in the system prompt.
"""

#separate func for evalution of resume
def evaluate_resume(resume_path: Path) -> ResumeEvaluation:
    resume_text = extract_resume_text(resume_path)
    user_prompt = build_user_prompt(resume_text)
    client = get_groq_client()

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            response_format=response_format,
        )
    except APIConnectionError as exc:
        raise RuntimeError(
            "Could not connect to Groq. Check your internet connection or firewall, then try again."
        ) from exc

    answer = response.choices[0].message.content
    return ResumeEvaluation.model_validate_json(answer)


def main() -> None:
    resume_path = BASE_DIR / "resumes" / "resume.pdf"
    try:
        evaluation = evaluate_resume(resume_path)
    except (FileNotFoundError, RuntimeError, ValueError, ValidationError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(evaluation.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
