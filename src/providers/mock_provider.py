"""
Mock LLM Provider Implementation
Provides realistic structured JSON evaluation fallbacks when no external server-side API keys are configured.
"""

import json
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
        else:  # Standard Resume Analysis
            p_hash = int(hashlib.md5(prompt.encode('utf-8')).hexdigest()[:8], 16)
            sf = 16 + (p_hash % 5)         # 16 - 20
            ts = 23 + ((p_hash >> 2) % 7)   # 23 - 29
            qr = 21 + ((p_hash >> 4) % 8)   # 21 - 28
            ef = 15 + ((p_hash >> 6) % 5)   # 15 - 19
            total_ats = sf + ts + qr + ef

            res = {
                "score_breakdown": {
                    "structure_formatting": sf,
                    "technical_skills": ts,
                    "quantifiable_results": qr,
                    "experience_fit": ef,
                },
                "ats_score": total_ats,
                "summary": "Accomplished Senior Software Engineer with strong experience in full stack application development, microservices, and AI integrations. Demonstrates track record of building high-performance systems and leading agile teams.",
                "technical_skills": ["Python", "FastAPI", "TypeScript", "React", "Docker", "PostgreSQL", "AWS"],
                "soft_skills": ["Technical Leadership", "Agile Collaboration", "System Design Thinking"],
                "missing_skills": ["Kubernetes", "GraphQL / gRPC"],
                "strengths": ["Quantifiable metric-driven bullet points", "Strong backend and database technical stack", "Clear structural formatting and contact layout"],
                "weaknesses": ["Could add Kubernetes orchestration experience", "Include additional industry certifications"],
                "improvement_suggestions": [
                    "Add quantifiable metrics to recent role accomplishments.",
                    "Highlight Kubernetes or container orchestration projects.",
                    "Include relevant cloud certifications (e.g. AWS Certified Developer).",
                ],
                "jd_match_score": min(95, total_ats + 1),
                "matching_keywords": ["Python", "FastAPI", "React", "PostgreSQL"],
                "missing_jd_keywords": ["Kubernetes", "Redis"],
                "jd_tailored_suggestions": ["Emphasize containerization and caching experience in work history."],
            }

        return json.dumps(res)
