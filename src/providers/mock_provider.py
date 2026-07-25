"""
Mock LLM Provider Implementation
Provides realistic structured JSON evaluation fallbacks when no external server-side API keys are configured.
"""

import json
import hashlib
from src.providers.base import BaseLLMProvider


class MockLLMProvider(BaseLLMProvider):
    """Mock AI Provider generating realistic structured JSON responses for local demo/testing."""

    def __init__(self) -> None:
        super().__init__(name="SaaS Demo AI Engine", default_model="saas-demo-v1")

    def generate(self, prompt: str, system_prompt: str, model_name: str | None = None) -> str:
        """Generates structured JSON based on prompt type."""
        prompt_upper = prompt.upper()

        if "COVER LETTER" in prompt_upper:
            res = {
                "cover_letter": "Dear Hiring Manager,\n\nI am writing to express my strong enthusiasm for the Software Engineering role. With proven experience building scalable microservices and AI integrations, I am confident in my ability to add immediate value to your team.\n\nThroughout my career, I have engineered high-throughput backend APIs and collaborated closely with product managers to deliver user-centric features. My technical foundation spans Python, cloud architecture, and modern DevOps practices.\n\nI welcome the opportunity to discuss how my technical skills and leadership experience align with your engineering goals. Thank you for your time and consideration.\n\nSincerely,\nCandidate",
                "key_highlights": ["Full Stack Engineering", "Cloud Microservices", "AI Systems Integration"],
            }
        elif "BULLET" in prompt_upper:
            res = {
                "original": "Worked on backend APIs",
                "rewrites": [
                    {"style": "Action & Metrics Heavy", "bullet": "Architected 12+ RESTful FastAPI backend microservices handling 1.5M+ daily requests with 99.9% uptime."},
                    {"style": "Leadership & Scale Focused", "bullet": "Spearheaded backend architecture overhaul, reducing response latency by 45% across core APIs."},
                    {"style": "Technical & Tool Focused", "bullet": "Containerized legacy monolithic services using Docker & Kubernetes on AWS ECS cluster."},
                ],
            }
        elif "INTERVIEW" in prompt_upper:
            res = {
                "technical_questions": [
                    {"question": "How do you optimize slow SQL queries in a PostgreSQL microservice backend?", "topic": "Database Performance", "answer_strategy": "Explain indexing strategies, EXPLAIN ANALYZE, and Redis caching."},
                    {"question": "What architecture pattern do you use for handling asynchronous background tasks?", "topic": "System Design", "answer_strategy": "Describe Celery/Redis task queues or AWS SQS worker loops."},
                ],
                "behavioral_questions": [
                    {"question": "Describe a time when you had to resolve a high-severity production outage.", "competency": "Incident Response", "star_framework": "Detail Situation, Task, Action taken, and Results with post-mortem metrics."},
                ],
            }
        elif "OUTREACH" in prompt_upper:
            res = {
                "recruiter_email": {
                    "subject": "Experienced Software Engineer | Application for Target Role",
                    "body": "Dear Talent Acquisition Team,\n\nI am writing to express my enthusiastic interest in software engineering opportunities at your company. With proven hands-on experience building scalable microservices, cloud infrastructure, and AI platform integrations, I am confident in my ability to bring immediate technical value to your team.\n\nThroughout my engineering career, I have designed high-throughput REST APIs, optimized SQL/NoSQL database performance, and delivered core production features in fast-paced agile environments. My background spans Python, TypeScript, React, Docker, and AWS, with a strong focus on system reliability and performance.\n\nI would love the opportunity to briefly connect and discuss how my technical background aligns with your engineering goals. Thank you for your time and consideration.\n\nSincerely,\nCandidate",
                },
                "hiring_manager_email": {
                    "subject": "Engineering Leadership & Microservices Expertise | Team Inquiry",
                    "body": "Dear Engineering Leader,\n\nI have been closely following your team's engineering work and technical accomplishments. As a Software Engineer specializing in backend system design, database optimization, and high-performance microservices, I am reaching out directly to explore synergies with your current roadmap.\n\nIn my previous roles, I spearheaded backend architecture overhauls that reduced request latency by 45% across core APIs while maintaining 99.9% uptime. I thrive in high-ownership technical environments focused on shipping clean, scalable, and well-tested code.\n\nI would welcome a brief 10-minute conversation to share technical insights and discuss how I can contribute to your engineering deliverables. Thank you for your time and leadership.\n\nBest regards,\nCandidate",
                },
                "linkedin_note": "Hi! Experienced Full Stack Software Engineer specializing in high-throughput backend microservices and AI integrations. I'd love to connect and follow your team's engineering work!",
            }
        elif "SALARY" in prompt_upper:
            if "INDIA" in prompt_upper or "INR" in prompt_upper or "₹" in prompt_upper:
                res = {
                    "currency": "₹ LPA (INR)",
                    "seniority_level": "Senior Software Engineer",
                    "estimated_min": "14.5 LPA",
                    "estimated_median": "24.0 LPA",
                    "estimated_max": "38.0 LPA",
                    "top_value_skills": ["Python", "FastAPI", "Cloud Architecture"],
                    "negotiation_leverage_points": ["High microservices throughput experience", "Proven system latency optimization"],
                }
            elif "UK" in prompt_upper or "GBP" in prompt_upper or "£" in prompt_upper:
                res = {
                    "currency": "£ GBP",
                    "seniority_level": "Senior Software Engineer",
                    "estimated_min": "£62,000",
                    "estimated_median": "£82,000",
                    "estimated_max": "£115,000",
                    "top_value_skills": ["Python", "FastAPI", "Cloud Architecture"],
                    "negotiation_leverage_points": ["Strong backend system architecture", "Proven production metrics"],
                }
            elif "EU" in prompt_upper or "EUROPE" in prompt_upper or "EUR" in prompt_upper or "€" in prompt_upper:
                res = {
                    "currency": "€ EUR",
                    "seniority_level": "Senior Software Engineer",
                    "estimated_min": "€58,000",
                    "estimated_median": "€78,000",
                    "estimated_max": "€105,000",
                    "top_value_skills": ["Python", "FastAPI", "Cloud Architecture"],
                    "negotiation_leverage_points": ["Strong backend system architecture", "Proven production metrics"],
                }
            else:
                res = {
                    "currency": "$ USD",
                    "seniority_level": "Senior Software Engineer",
                    "estimated_min": "$125,000",
                    "estimated_median": "$160,000",
                    "estimated_max": "$195,000",
                    "top_value_skills": ["Python", "FastAPI", "Cloud Architecture"],
                    "negotiation_leverage_points": ["Strong microservices experience", "Proven latency reduction metrics"],
                }
        else:  # Standard Resume Analysis - Intelligent Real-Text Heuristic Parser
            import re

            resume_text = prompt
            if "RESUME TEXT:" in prompt:
                resume_text = prompt.split("RESUME TEXT:", 1)[1]

            cleaned_lower = resume_text.lower()

            KNOWN_TECH_SKILLS = [
                "Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "React", "Angular", "Vue", "Node.js",
                "Express", "Django", "Flask", "FastAPI", "Spring Boot", "SQL", "PostgreSQL", "MySQL", "MongoDB",
                "Redis", "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Git", "Linux", "REST", "GraphQL", "gRPC",
                "Microservices", "CI/CD", "HTML", "CSS", "Tailwind", "Bootstrap", "PyTorch", "TensorFlow", "Pandas",
                "NumPy", "Scikit-Learn", "OpenCV", "Kafka", "Elasticsearch", "Jenkins", "Terraform", "Ansible"
            ]
            KNOWN_SOFT_SKILLS = [
                "Technical Leadership", "Agile Methodologies", "Cross-Functional Collaboration", "Problem Solving",
                "System Design", "Code Review", "Project Management", "Team Mentorship", "Stakeholder Communication"
            ]

            def _check_skill(s_name: str) -> bool:
                s_low = s_name.lower()
                if any(char in s_low for char in ["+", "#", "/", "."]):
                    return s_low in cleaned_lower
                return bool(re.search(r'\b' + re.escape(s_low) + r'\b', cleaned_lower))

            found_tech = [s for s in KNOWN_TECH_SKILLS if _check_skill(s)]
            found_soft = [s for s in KNOWN_SOFT_SKILLS if _check_skill(s)]

            metrics_found = re.findall(r'(\d+%\s*|\$\d+[\d,]*|\b\d+\+\s*(?:users|requests|clients|projects|million|k|m|%)|\b\d{2,}\b)', cleaned_lower)
            metric_count = len(metrics_found)

            has_email = "@" in cleaned_lower
            has_phone = bool(re.search(r'\b\d{10}\b|\+\d{1,3}', cleaned_lower))
            has_linkedin = "linkedin" in cleaned_lower

            sf = 12
            if has_email: sf += 3
            if has_phone: sf += 2
            if has_linkedin: sf += 3
            sf = min(20, sf)

            ts = min(30, max(8, len(found_tech) * 3))

            if metric_count >= 5:
                qr = min(30, 18 + metric_count * 2)
            elif metric_count >= 2:
                qr = 14 + metric_count * 2
            else:
                qr = max(5, metric_count * 4)

            ef = min(20, 10 + min(10, len(resume_text) // 250))
            total_ats = sf + ts + qr + ef

            all_possible_missing = ["Docker", "Kubernetes", "AWS", "CI/CD", "Redis", "TypeScript", "System Design"]
            missing_skills = [m for m in all_possible_missing if m not in found_tech][:3]
            if not missing_skills:
                missing_skills = ["Advanced Cloud Architecture", "gRPC Microservices"]

            strengths = []
            if found_tech:
                strengths.append(f"Strong technical stack detected: {', '.join(found_tech[:4])}")
            if metric_count >= 2:
                strengths.append(f"Includes quantifiable achievements and metrics ({metric_count} metric points found)")
            if sf >= 16:
                strengths.append("Clean document structure with complete contact information")
            if not strengths:
                strengths = ["Clear professional experience section", "Readable layout structure"]

            weaknesses = []
            if metric_count < 3:
                weaknesses.append("Lacks sufficient quantifiable impact metrics (percentages %, dollar values $, or throughput numbers)")
            if ts < 18:
                weaknesses.append("Technical skill inventory could be expanded to match industry roles")
            if not has_linkedin:
                weaknesses.append("Missing explicit LinkedIn profile link in contact section")
            if not weaknesses:
                weaknesses = ["Could include additional industry certifications", "Emphasize leadership experience"]

            improvement_suggestions = [
                "Quantify bullet points with measurable impact (e.g., 'Improved latency by 35%' or 'Handled 50k+ daily users').",
                "Highlight core technical frameworks near the top of your experience bullets.",
                "Ensure standard contact details (Email, Phone, LinkedIn, GitHub) are clearly visible at the top."
            ]

            tech_summary_str = f" possessing technical experience in {', '.join(found_tech[:3])}" if found_tech else ""
            summary = f"Evaluated candidate resume{tech_summary_str}. Demonstrates a structured professional background with an overall ATS compatibility score of {total_ats}/100."

            res = {
                "score_breakdown": {
                    "structure_formatting": sf,
                    "technical_skills": ts,
                    "quantifiable_results": qr,
                    "experience_fit": ef,
                },
                "ats_score": total_ats,
                "summary": summary,
                "technical_skills": found_tech if found_tech else ["Software Development", "Database Management"],
                "soft_skills": found_soft if found_soft else ["Problem Solving", "Team Collaboration"],
                "missing_skills": missing_skills,
                "strengths": strengths,
                "weaknesses": weaknesses,
                "improvement_suggestions": improvement_suggestions,
                "jd_match_score": min(95, total_ats) if "JOB DESCRIPTION:" in prompt else 0,
                "matching_keywords": found_tech[:3] if found_tech else ["Software"],
                "missing_jd_keywords": missing_skills[:2],
                "jd_tailored_suggestions": ["Align resume key terms directly with target job requirements."],
            }

        return json.dumps(res)
