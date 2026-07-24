"""
Utility Functions Module
Helper utilities for text cleaning, file validation, sample loader, and report formatting.
"""

import json
import os
import re
from src.config import config


def is_valid_file_extension(filename: str) -> bool:
    """
    Checks if the uploaded file has a supported extension (.pdf or .docx).

    Args:
        filename: Name of the file.

    Returns:
        bool: True if extension is valid, False otherwise.
    """
    ext = os.path.splitext(filename)[1].lower()
    return ext in config.ALLOWED_EXTENSIONS


def is_valid_file_size(file_bytes: bytes) -> bool:
    """
    Checks if the file size is within the allowed limit.

    Args:
        file_bytes: Raw bytes of the file.

    Returns:
        bool: True if size is valid, False otherwise.
    """
    max_bytes = config.MAX_FILE_SIZE_MB * 1024 * 1024
    return len(file_bytes) <= max_bytes


def clean_text(text: str) -> str:
    """
    Sanitizes and cleans extracted text from documents.

    Args:
        text: Raw text string.

    Returns:
        str: Cleaned and normalized text string.
    """
    if not text:
        return ""

    # Replace non-breaking spaces and normalize whitespace/newlines
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def get_sample_resume_text() -> tuple[str, str, str]:
    """
    Returns a sample production resume text, filename, and target job description for 1-click testing.

    Returns:
        tuple[str, str, str]: (sample_text, sample_filename, sample_jd)
    """
    sample_text = """
ALEXANDER PIERCE
Senior Full Stack Engineer & Cloud Architect
Email: alexander.pierce@email.com | Phone: +1 (555) 019-2834 | GitHub: github.com/alex-pierce | LinkedIn: linkedin.com/in/alexpierce

PROFESSIONAL SUMMARY:
Results-driven Senior Full Stack Engineer with 7+ years of experience building scalable microservices, AI-powered applications, and enterprise web platforms. Skilled in Python, TypeScript, React, Docker, Kubernetes, and Cloud Architecture (AWS/GCP). Proven track record of reducing latency by 45% and leading cross-functional engineering teams.

TECHNICAL SKILLS:
• Programming Languages: Python, TypeScript, JavaScript, SQL, Go
• Frameworks & Web: FastAPI, Django, React, Next.js, Node.js, Streamlit
• Cloud & DevOps: AWS (EC2, S3, Lambda, ECS), Docker, Kubernetes, CI/CD (GitHub Actions), Terraform
• AI & Databases: PostgreSQL, Redis, MongoDB, Google Gemini API, OpenAI API, LangChain

WORK EXPERIENCE:
Senior Software Engineer | CloudTech Solutions (2021 - Present)
• Architected and deployed microservice backend handling 2.5M+ daily requests using FastAPI, Docker, and AWS ECS.
• Improved API response times by 40% by implementing Redis caching and optimizing PostgreSQL query execution plans.
• Mentored 6 junior engineers and spearheaded adoption of modern CI/CD pipelines, reducing deployment times from 45 to 10 minutes.
• Integrated Google Gemini Generative API to automate internal customer support ticket routing, cutting resolution time by 30%.

Full Stack Developer | NexaDigital Systems (2018 - 2021)
• Developed responsive frontend dashboard using React and Redux, serving 150,000+ monthly active users.
• Built RESTful APIs using Python Django and integrated Stripe payment gateway, processing $1.2M in annual transactions.
• Containerized legacy monolithic application using Docker and deployed to AWS EC2 cluster.

EDUCATION & CERTIFICATIONS:
• Bachelor of Science in Computer Science | University of Technology (2014 - 2018)
• AWS Certified Solutions Architect – Associate (2022)
"""
    sample_jd = """
We are looking for a Senior Full Stack Engineer to lead our AI Platform team.
Required Qualifications:
- 5+ years experience with Python (FastAPI/Django) and TypeScript/React.
- Hands-on experience deploying containerized applications with Docker & Kubernetes on AWS.
- Background in integrating AI/LLM APIs (Gemini, OpenAI) into production web apps.
- Strong knowledge of PostgreSQL, Redis caching, and CI/CD pipelines.
"""
    return sample_text.strip(), "sample_alexander_pierce_resume.pdf", sample_jd.strip()


def generate_json_report(analysis_result: dict) -> str:
    """
    Formats the analysis result dictionary into a pretty-printed JSON string.

    Args:
        analysis_result: Result dictionary from ResumeAnalyzer.

    Returns:
        str: Pretty-printed JSON string.
    """
    return json.dumps(analysis_result, indent=2, ensure_ascii=False)


def generate_text_report(analysis_result: dict) -> str:
    """
    Formats the analysis result dictionary into a clean, human-readable text report.

    Args:
        analysis_result: Result dictionary from ResumeAnalyzer.

    Returns:
        str: Formatted plain text evaluation report.
    """
    meta = analysis_result.get("meta", {})
    score = analysis_result.get("ats_score", 0)
    summary = analysis_result.get("summary", "N/A")
    tech_skills = ", ".join(analysis_result.get("technical_skills", [])) or "None detected"
    soft_skills = ", ".join(analysis_result.get("soft_skills", [])) or "None detected"
    missing_skills = ", ".join(analysis_result.get("missing_skills", [])) or "None identified"

    strengths = "\n".join([f"  • {item}" for item in analysis_result.get("strengths", [])]) or "  None listed"
    weaknesses = "\n".join([f"  • {item}" for item in analysis_result.get("weaknesses", [])]) or "  None listed"
    suggestions = "\n".join([f"  {idx}. {item}" for idx, item in enumerate(analysis_result.get("improvement_suggestions", []), 1)]) or "  None listed"

    report_lines = [
        "================================================================================",
        "                        AI RESUME EVALUATION REPORT                             ",
        "================================================================================",
        f"Document Name : {meta.get('filename', 'N/A')}",
        f"Target Role   : {meta.get('target_role', 'General Tech')}",
        f"ATS Score     : {score}/100",
        "--------------------------------------------------------------------------------",
        "1. EXECUTIVE SUMMARY",
        "--------------------------------------------------------------------------------",
        f"{summary}",
        "",
        "--------------------------------------------------------------------------------",
        "2. SKILLS TAXONOMY ASSESSMENT",
        "--------------------------------------------------------------------------------",
        f"Technical Skills : {tech_skills}",
        f"Soft Skills      : {soft_skills}",
        f"Missing Skills   : {missing_skills}",
        "",
        "--------------------------------------------------------------------------------",
        "3. STRENGTHS & AREAS FOR IMPROVEMENT",
        "--------------------------------------------------------------------------------",
        "KEY STRENGTHS:",
        f"{strengths}",
        "",
        "AREAS FOR IMPROVEMENT:",
        f"{weaknesses}",
        "",
        "--------------------------------------------------------------------------------",
        "4. ACTIONABLE IMPROVEMENT RECOMMENDATIONS",
        "--------------------------------------------------------------------------------",
        f"{suggestions}",
    ]

    # Include Job Description section if present
    if meta.get("has_jd") or analysis_result.get("jd_match_score", 0) > 0:
        jd_score = analysis_result.get("jd_match_score", 0)
        matched_kw = ", ".join(analysis_result.get("matching_keywords", [])) or "None"
        missing_kw = ", ".join(analysis_result.get("missing_jd_keywords", [])) or "None"
        jd_sug = "\n".join([f"  {idx}. {item}" for idx, item in enumerate(analysis_result.get("jd_tailored_suggestions", []), 1)]) or "  None"

        report_lines.extend([
            "",
            "--------------------------------------------------------------------------------",
            "5. TARGET JOB DESCRIPTION MATCH ANALYSIS",
            "--------------------------------------------------------------------------------",
            f"JD Match Score        : {jd_score}%",
            f"Matching Keywords     : {matched_kw}",
            f"Missing JD Keywords   : {missing_kw}",
            "",
            "JD TAILORED RECOMMENDATIONS:",
            f"{jd_sug}",
        ])

    report_lines.extend([
        "================================================================================",
        "               REPORT GENERATED BY PORTFOLIO AI RESUME ANALYZER                ",
        "================================================================================",
    ])

    return "\n".join(report_lines)
