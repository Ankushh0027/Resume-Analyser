"""
Prompts Module
Defines system instructions, prompt templates, and JSON response schemas for Gemini API.
"""

SYSTEM_INSTRUCTION = """
You are an expert ATS (Applicant Tracking System) Specialist and Senior Executive Technical Recruiter.
Your job is to analyze resumes objectively, extract key skills, calculate an accurate ATS compatibility score, identify strengths and weaknesses, and provide actionable improvement recommendations.

Always produce output in strict, valid JSON format matching the requested schema exactly.
Do not include markdown code block syntax (```json ... ```) or conversational preamble in your final response—only return the raw JSON object.
"""

RESUME_ANALYSIS_SCHEMA = {
    "ats_score": "Integer between 0 and 100 representing overall resume quality and ATS formatting readiness",
    "summary": "String providing a concise 3-4 sentence professional evaluation of the candidate",
    "technical_skills": "List of strings containing hard/technical skills, tools, programming languages, and frameworks found",
    "soft_skills": "List of strings containing soft skills, leadership traits, and communication capabilities found",
    "missing_skills": "List of strings containing industry-standard or expected technical/soft skills missing from the resume",
    "strengths": "List of 3-5 strings highlighting key candidate strengths and competitive advantages",
    "weaknesses": "List of 3-5 strings identifying weaknesses, vagueness, or formatting flaws",
    "improvement_suggestions": "List of 4-6 strings offering concrete, actionable steps to upgrade the resume impact"
}


def build_resume_analysis_prompt(resume_text: str, target_role: str = "") -> str:
    """
    Constructs the prompt payload for the Gemini API.

    Args:
        resume_text: Extracted plain text from candidate's resume.
        target_role: Optional target job title or industry focus.

    Returns:
        str: Fully formatted prompt string.
    """
    target_role_section = (
        f"\nTARGET JOB ROLE / INDUSTRY: {target_role.strip()}\n"
        if target_role and target_role.strip()
        else ""
    )

    prompt = f"""
Analyze the following resume text as an expert ATS auditor and technical recruiter.
{target_role_section}
RESUME TEXT:
----------------------------------------
{resume_text}
----------------------------------------

Generate a detailed evaluation in valid JSON matching this exact structure:
{{
  "ats_score": <number 0-100>,
  "summary": "<3-4 sentence professional candidate summary>",
  "technical_skills": ["<skill1>", "<skill2>", ...],
  "soft_skills": ["<skill1>", "<skill2>", ...],
  "missing_skills": ["<missing1>", "<missing2>", ...],
  "strengths": ["<strength1>", "<strength2>", ...],
  "weaknesses": ["<weakness1>", "<weakness2>", ...],
  "improvement_suggestions": ["<suggestion1>", "<suggestion2>", ...]
}}

CRITICAL INSTRUCTIONS:
1. Calculate 'ats_score' based on skill density, clarity, quantifiable metrics, and structure.
2. Return ONLY valid, parseable JSON. Do NOT wrap in markdown backticks or extra commentary.
"""
    return prompt.strip()
