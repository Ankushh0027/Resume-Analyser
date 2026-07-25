"""
Prompts Module
Defines system instructions, prompt templates, and JSON response schemas for Gemini API.
Optimized for high token efficiency and structured output precision.
"""

from src.utils import clean_text

SYSTEM_INSTRUCTION = """You are a rigorous, highly objective ATS Recruiter & Talent Audit Engine. Evaluate resumes with strict realism and 100% fairness. Do NOT give unearned high scores.

STRICT 100-PT RUBRIC SCORING GUIDELINES:
- structure_formatting (0-20): Standard headings, clean contact info, readable structure. (0-8 if missing contact info or disorganized).
- technical_skills (0-30): Hard technical skills, frameworks, tools explicitly present in resume text. (0-10 if vague or missing tech stack).
- quantifiable_results (0-30): Measurable impact, percentages (%), metrics, $, numbers. (0-5 if resume lacks numbers or metrics!).
- experience_fit (0-20): Career progression, relevant experience level for target role. (0-8 if weak or entry-level without relevance).

GRADING DISTRIBUTION CRITERIA:
- 30-55: Weak / Unformatted / Missing metrics & skills.
- 56-74: Average resume with basic skills but missing quantifiable impact.
- 75-89: Strong candidate with proven metrics and clear tech stack.
- 90-100: Top 1% Executive/Senior resume with outstanding STAR metrics.

CRITICAL: Calculate 'score_breakdown' FIRST. Set 'ats_score' to the exact sum of breakdown scores. Return raw JSON ONLY without markdown fences."""


def build_resume_analysis_prompt(
    resume_text: str,
    target_role: str = "",
    job_description: str = "",
) -> str:
    """Constructs token-efficient prompt for full ATS Resume Analysis."""
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description) if job_description else ""

    role_str = f"TARGET ROLE: {target_role.strip()}\n" if target_role and target_role.strip() else ""
    jd_str = f"JOB DESCRIPTION:\n{cleaned_jd}\n\n" if cleaned_jd else ""

    return f"""Analyze resume text as a rigorous, objective ATS Recruiter.
{role_str}{jd_str}RESUME TEXT:
{cleaned_resume}

Evaluate 100-pt rubric strictly based ONLY on the provided text:
- structure_formatting (0-20)
- technical_skills (0-30)
- quantifiable_results (0-30): Give low points (0-5) if text has no numbers, %, or metrics!
- experience_fit (0-20)

Return valid JSON structure:
{{
  "score_breakdown": {{
    "structure_formatting": <number 0 to 20>,
    "technical_skills": <number 0 to 30>,
    "quantifiable_results": <number 0 to 30>,
    "experience_fit": <number 0 to 20>
  }},
  "ats_score": <exact sum of the 4 score_breakdown numbers above, 0 to 100>,
  "summary": "<candidate summary based ONLY on resume text>",
  "technical_skills": ["<skill1>", "<skill2>"],
  "soft_skills": ["<skill1>", "<skill2>"],
  "missing_skills": ["<missing1>"],
  "strengths": ["<strength1>", "<strength2>"],
  "weaknesses": ["<weakness1>", "<weakness2>"],
  "improvement_suggestions": ["<suggestion1>", "<suggestion2>"],
  "jd_match_score": <match percentage 0-100 or 0 if no JD>,
  "matching_keywords": ["<matched1>"],
  "missing_jd_keywords": ["<missing1>"],
  "jd_tailored_suggestions": ["<suggestion1>"]
}}

CRITICAL: Be completely objective and fair. 'ats_score' MUST equal exact sum of breakdown numbers. Extract ONLY skills explicitly present in resume. Return ONLY raw JSON.""".strip()


def build_cover_letter_prompt(
    resume_text: str,
    target_role: str = "",
    job_description: str = "",
) -> str:
    """Constructs token-efficient prompt for AI Cover Letter generation."""
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description) if job_description else "General Role"
    role_str = target_role.strip() if target_role and target_role.strip() else "Software Professional"

    return f"""Write a 3-paragraph persuasive Cover Letter.
TARGET ROLE: {role_str}
JOB DESCRIPTION: {cleaned_jd}
RESUME TEXT:
{cleaned_resume}

Return ONLY valid JSON:
{{
  "cover_letter": "<full_text_with_newlines>",
  "key_highlights": ["<highlight1>", "<highlight2>", "<highlight3>"]
}}""".strip()


def build_bullet_enhancer_prompt(bullet_text: str, target_role: str = "") -> str:
    """Constructs prompt for AI Bullet Point Rewriter & Action Verb Enhancer."""
    cleaned_bullet = clean_text(bullet_text)
    role_str = target_role.strip() if target_role and target_role.strip() else "Software Engineer"

    return f"""Rewrite weak resume bullet point into 3 high-impact quantified achievements (Google XYZ formula).
TARGET ROLE: {role_str}
ORIGINAL BULLET: "{cleaned_bullet}"

Return ONLY valid JSON:
{{
  "original": "{cleaned_bullet}",
  "rewrites": [
    {{"style": "Action & Metrics Heavy", "bullet": "<bullet_1>"}},
    {{"style": "Leadership & Scale Focused", "bullet": "<bullet_2>"}},
    {{"style": "Technical & Tool Focused", "bullet": "<bullet_3>"}}
  ]
}}""".strip()


def build_interview_predictor_prompt(
    resume_text: str,
    target_role: str = "",
    job_description: str = "",
) -> str:
    """Constructs prompt for AI Mock Interview Question Predictor."""
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description) if job_description else "Tech Role"
    role_str = target_role.strip() if target_role and target_role.strip() else "Software Engineer"

    return f"""Predict 5 Technical and 5 Behavioral STAR interview questions based on resume & role.
TARGET ROLE: {role_str}
JOB DESCRIPTION: {cleaned_jd}
RESUME TEXT: {cleaned_resume}

Return ONLY valid JSON:
{{
  "technical_questions": [
    {{"question": "<question>", "topic": "<topic>", "answer_strategy": "<strategy>"}}
  ],
  "behavioral_questions": [
    {{"question": "<question>", "competency": "<competency>", "star_framework": "<guidance>"}}
  ]
}}""".strip()


def build_outreach_prompt(
    resume_text: str,
    target_role: str = "",
    company_name: str = "",
    job_description: str = "",
) -> str:
    """Constructs prompt for high-converting Recruiter Cold Email, Hiring Manager Email & LinkedIn Outreach Generator."""
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(job_description) if job_description else "Engineering Role"
    role_str = target_role.strip() if target_role and target_role.strip() else "Software Engineer"
    comp_str = company_name.strip() if company_name and company_name.strip() else "Target Company"

    return f"""You are a world-class Executive Career Coach and Technical Recruiter. Write 3 highly personalized, high-converting cold outreach messages for the candidate.

INPUT DATA:
- TARGET ROLE: {role_str}
- TARGET COMPANY: {comp_str}
- JOB DESCRIPTION: {cleaned_jd}
- CANDIDATE RESUME TEXT:
{cleaned_resume}

GUIDELINES FOR OUTREACH TEMPLATES:
1. recruiter_email:
   - Subject line: High-open rate, professional subject line mentioning candidate's primary skill stack and the role at {comp_str}.
   - Body (3 paragraphs):
     * Para 1: Enthusiastic hook referencing {comp_str} and the {role_str} position, citing candidate's top 3 technical skills from resume.
     * Para 2: Specific quantified metric/achievement extracted from candidate's resume history.
     * Para 3: Polite, low-friction Call-To-Action asking for a brief 10-minute discovery call.

2. hiring_manager_email:
   - Subject line: Engineering-focused, value-driven subject line.
   - Body (3 paragraphs):
     * Para 1: Peer-to-peer technical hook explaining candidate's interest in {comp_str}'s engineering vision.
     * Para 2: Highlights technical problem-solving capabilities, backend/frontend microservices scale, and architecture experience.
     * Para 3: Professional call-to-action to share technical insights.

3. linkedin_note:
   - Concise connection request note (< 280 characters) mentioning target role and top skill.

Return ONLY valid JSON:
{{
  "recruiter_email": {{
    "subject": "<high_converting_subject>",
    "body": "<full_3_paragraph_email_text>"
  }},
  "hiring_manager_email": {{
    "subject": "<value_driven_subject>",
    "body": "<full_3_paragraph_email_text>"
  }},
  "linkedin_note": "<short_note_under_280_chars>"
}}""".strip()


def build_salary_estimation_prompt(
    resume_text: str,
    target_role: str = "",
    target_location: str = "United States (USD $)",
    company_tier: str = "Mid-Size IT Enterprise",
) -> str:
    """Constructs prompt for Region & Company-Tier adjusted Salary Range & Compensation Leverage Estimator."""
    cleaned_resume = clean_text(resume_text)
    role_str = target_role.strip() if target_role and target_role.strip() else "Software Engineer"
    loc_str = target_location.strip() if target_location else "United States (USD $)"
    tier_str = company_tier.strip() if company_tier else "Mid-Size IT Enterprise"

    return f"""Estimate realistic market salary range adjusted for candidate experience, location/country, and company tier.

INPUT PARAMETERS:
- TARGET ROLE: {role_str}
- TARGET COUNTRY / REGION: {loc_str}
- COMPANY TIER / TYPE: {tier_str}
- CANDIDATE RESUME TEXT:
{cleaned_resume}

GUIDELINES:
1. Currency & Unit: Use local currency symbol (e.g. ₹ INR in Lakhs per annum for India, $ USD for US/Canada/Remote, £ GBP for UK, € EUR for EU).
2. Realistic Market Adjustments:
   - India: Express in Lakhs Per Annum (e.g. min: 14.5 LPA, median: 24.0 LPA, max: 40.0 LPA).
   - US / UK / EU / Canada: Express in annual base salary.
   - Company Tier: FAANG/Unicorn pays higher equity/base than early startups or local agencies.

Return ONLY valid JSON:
{{
  "currency": "<currency symbol e.g. ₹ LPA, $ USD, £ GBP, € EUR>",
  "seniority_level": "<Seniority Level e.g. Senior Engineer>",
  "estimated_min": "<number or formatted string e.g. 14.5 LPA or 120000>",
  "estimated_median": "<number or formatted string e.g. 24.0 LPA or 160000>",
  "estimated_max": "<number or formatted string e.g. 38.0 LPA or 195000>",
  "top_value_skills": ["<skill1>", "<skill2>", "<skill3>"],
  "negotiation_leverage_points": ["<point1>", "<point2>", "<point3>"]
}}""".strip()
