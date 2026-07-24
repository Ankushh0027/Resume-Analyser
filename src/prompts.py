"""
Prompts Module
Defines system instructions, prompt templates, and JSON response schemas for Gemini API.
"""

SYSTEM_INSTRUCTION = """
You are an expert ATS (Applicant Tracking System) Specialist and Senior Executive Technical Recruiter.
Your job is to analyze resumes objectively, extract key skills, calculate an accurate ATS compatibility score using a strict 100-point rubric, identify strengths and weaknesses, compare resumes against job descriptions when provided, and provide actionable improvement recommendations.

SCORING RUBRIC (STRICT 100 POINTS):
- Structure & Formatting (Max 20 pts): Clear sections, readable layout, contact details, standard headings.
- Technical & Hard Skills (Max 30 pts): Hard skills, frameworks, tools, programming languages.
- Quantifiable Results (Max 30 pts): Metrics, percentages, numbers, business impact statements.
- Experience & Role Fit (Max 20 pts): Work history progression, relevant experience, education, certs.

CRITICAL ORDER REQUIREMENT:
You MUST calculate and output the 'score_breakdown' object FIRST.
Then set 'ats_score' to the exact sum of (structure_formatting + technical_skills + quantifiable_results + experience_fit).

Always produce output in strict, valid JSON format matching the requested schema exactly.
Do not include markdown code block syntax (```json ... ```) or conversational preamble in your final response—only return the raw JSON object.
"""

RESUME_ANALYSIS_SCHEMA = {
    "score_breakdown": {
        "structure_formatting": "Integer (0-20)",
        "technical_skills": "Integer (0-30)",
        "quantifiable_results": "Integer (0-30)",
        "experience_fit": "Integer (0-20)"
    },
    "ats_score": "Exact sum of the 4 breakdown scores (0-100)",
    "summary": "String providing a concise 3-4 sentence professional evaluation of the candidate",
    "technical_skills": "List of strings containing hard/technical skills, tools, programming languages, and frameworks found",
    "soft_skills": "List of strings containing soft skills, leadership traits, and communication capabilities found",
    "missing_skills": "List of strings containing industry-standard or expected technical/soft skills missing from the resume",
    "strengths": "List of 3-5 strings highlighting key candidate strengths and competitive advantages",
    "weaknesses": "List of 3-5 strings identifying weaknesses, vagueness, or formatting flaws",
    "improvement_suggestions": "List of 4-6 strings offering concrete, actionable steps to upgrade the resume impact",
    "jd_match_score": "Integer between 0 and 100 comparing resume alignment against target Job Description (0 if no JD provided)",
    "matching_keywords": "List of strings containing key terms/skills present in both the resume and the Job Description",
    "missing_jd_keywords": "List of strings containing critical terms/skills required in the Job Description but missing from the resume",
    "jd_tailored_suggestions": "List of strings offering specific recommendations to tailor the resume to the target Job Description"
}


def build_resume_analysis_prompt(
    resume_text: str,
    target_role: str = "",
    job_description: str = "",
) -> str:
    """Constructs the prompt payload for the Gemini API using Chain-of-Thought scoring breakdown."""
    target_role_section = (
        f"\nTARGET JOB ROLE / INDUSTRY: {target_role.strip()}\n"
        if target_role and target_role.strip()
        else ""
    )

    jd_section = (
        f"\nTARGET JOB DESCRIPTION:\n----------------------------------------\n{job_description.strip()}\n----------------------------------------\n"
        if job_description and job_description.strip()
        else ""
    )

    prompt = f"""
Analyze the following resume text as an expert ATS auditor and technical recruiter.
{target_role_section}
RESUME TEXT:
----------------------------------------
{resume_text}
----------------------------------------
{jd_section}

Evaluate step-by-step using the 100-point rubric:
1. structure_formatting (0-20)
2. technical_skills (0-30)
3. quantifiable_results (0-30)
4. experience_fit (0-20)

Generate a detailed evaluation in valid JSON matching this exact structure:
{{
  "score_breakdown": {{
    "structure_formatting": <number 0-20>,
    "technical_skills": <number 0-30>,
    "quantifiable_results": <number 0-30>,
    "experience_fit": <number 0-20>
  }},
  "ats_score": <sum of the 4 breakdown category points above, number 0-100>,
  "summary": "<3-4 sentence professional candidate summary>",
  "technical_skills": ["<skill1>", "<skill2>", ...],
  "soft_skills": ["<skill1>", "<skill2>", ...],
  "missing_skills": ["<missing1>", "<missing2>", ...],
  "strengths": ["<strength1>", "<strength2>", ...],
  "weaknesses": ["<weakness1>", "<weakness2>", ...],
  "improvement_suggestions": ["<suggestion1>", "<suggestion2>", ...],
  "jd_match_score": <number 0-100, calculate match against target Job Description, or 0 if no JD provided>,
  "matching_keywords": ["<matched_keyword1>", "<matched_keyword2>", ...],
  "missing_jd_keywords": ["<missing_jd_keyword1>", "<missing_jd_keyword2>", ...],
  "jd_tailored_suggestions": ["<tailored_suggestion1>", "<tailored_suggestion2>", ...]
}}

CRITICAL INSTRUCTIONS:
1. You MUST generate 'score_breakdown' FIRST before 'ats_score'.
2. Set 'ats_score' to the exact sum of the 4 sub-scores.
3. Return ONLY valid, parseable JSON. Do NOT wrap in markdown backticks or extra commentary.
"""
    return prompt.strip()


def build_cover_letter_prompt(
    resume_text: str,
    target_role: str = "",
    job_description: str = "",
) -> str:
    """Constructs prompt for AI Cover Letter generation."""
    return f"""
You are an executive career coach and professional copywriter.
Write a highly persuasive, 3-paragraph professional Cover Letter for the candidate based on their resume and target job.

TARGET ROLE: {target_role if target_role else 'Software / Tech Professional'}
JOB DESCRIPTION: {job_description if job_description else 'General Software Engineering Role'}

RESUME TEXT:
{resume_text}

INSTRUCTIONS:
1. Paragraph 1: High-impact opening line introducing the candidate, target role, and enthusiasm for the company mission.
2. Paragraph 2: Core technical achievements from the resume directly mapped to the job requirements, highlighting quantified metrics.
3. Paragraph 3: Professional call-to-action expressing desire for an interview.
4. Return ONLY valid JSON with structure:
{{
  "cover_letter": "<full_cover_letter_text_with_newlines>",
  "key_highlights": ["<highlight1>", "<highlight2>", "<highlight3>"]
}}
""".strip()


def build_bullet_enhancer_prompt(bullet_text: str, target_role: str = "") -> str:
    """Constructs prompt for AI Bullet Point Rewriter & Action Verb Enhancer."""
    return f"""
You are a Senior Recruiter at a Top Tech Company (FAANG/MAANG).
Rewrite the following weak resume bullet point into 3 high-impact, quantified achievement bullet points.

TARGET ROLE: {target_role if target_role else 'Software Engineer'}
ORIGINAL BULLET POINT:
"{bullet_text}"

INSTRUCTIONS:
- Use strong action verbs (Architected, Engineered, Spearheaded, Optimized).
- Include realistic quantified impact metrics (percentages, throughput, latency, revenue/cost savings).
- Follow the Google XYZ resume formula: "Accomplished [X] as measured by [Y], by doing [Z]".
- Return ONLY valid JSON with structure:
{{
  "original": "{bullet_text}",
  "rewrites": [
    {{"style": "Action & Metrics Heavy", "bullet": "<enhanced_bullet_1>"}},
    {{"style": "Leadership & Scale Focused", "bullet": "<enhanced_bullet_2>"}},
    {{"style": "Technical & Tool Focused", "bullet": "<enhanced_bullet_3>"}}
  ]
}}
""".strip()


def build_interview_predictor_prompt(
    resume_text: str,
    target_role: str = "",
    job_description: str = "",
) -> str:
    """Constructs prompt for AI Mock Interview Question Predictor."""
    return f"""
You are a Principal Engineering Manager conducting technical and behavioral interviews.
Based on the candidate's resume and target role/JD, predict 5 Technical Questions and 5 Behavioral STAR Questions they will likely face in real interviews, along with ideal sample answer strategies.

TARGET ROLE: {target_role if target_role else 'Software Engineer'}
JOB DESCRIPTION: {job_description if job_description else 'Tech Role'}
RESUME TEXT:
{resume_text}

Return ONLY valid JSON with structure:
{{
  "technical_questions": [
    {{"question": "<tech_question_1>", "topic": "<topic>", "answer_strategy": "<key_points_to_mention>"}},
    ... (5 total)
  ],
  "behavioral_questions": [
    {{"question": "<behavioral_star_question_1>", "competency": "<competency>", "star_framework": "<situation_task_action_result_guidance>"}},
    ... (5 total)
  ]
}}
""".strip()
