# AI Resume Analyzer & Career Intelligence Suite ⚡

[![Python Version](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![AI Engine](https://img.shields.io/badge/Multi--Provider-Gemini%20%7C%20OpenRouter%20%7C%20OpenAI-4285F4.svg?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Database](https://img.shields.io/badge/Database-SQLite%203-003B57.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

An enterprise-grade platform for **AI Resume Auditing, Regional Salary Estimations, Cover Letter Generation, Bullet Rewriting, Recruiter Outreach, and Mock Interview Prediction**.

---

## 🌟 Key Features

1. **📊 AI Resume Analyzer**:
   - **4 Core Rubrics**: Formatting (20 pts), Technical Stack (30 pts), Quantifiable Metrics (30 pts), Experience Fit (20 pts).
   - **Deterministic ATS Scoring**: Consistent MD5 content hashing ensures identical scores for identical resumes.
   - **Keyword Match**: Extracted technical skills, soft skills, missing skills, strengths, weaknesses, and pre-application checklist.

2. **💼 Region & Company-Tier Salary Estimator**:
   - Region-accurate market compensation ranges across **India (INR ₹ LPA)**, **United States ($ USD)**, **United Kingdom (£ GBP)**, **European Union (€ EUR)**, **Canada**, **Australia**, and **Global Remote**.
   - Tier compensation adjustments for **FAANG giants**, **Scaleups**, **MNCs**, **Startups**, and **Agencies**.

3. **📝 Executive Cover Letter Generator**:
   - Generates custom, 3-paragraph executive cover letters tailored to target job descriptions with download support.

4. **⚡ Bullet Point Enhancer**:
   - Converts weak bullet points into high-impact, STAR-formatted statements with action verbs and quantifiable metrics.

5. **🆚 Resume A/B Version Comparison**:
   - Evaluates two resume versions side-by-side to highlight score deltas and skill improvements.

6. **🎯 Mock Interview Question Predictor**:
   - Predicts role-specific technical deep-dive questions and STAR behavioral scenarios.

7. **📧 Recruiter & Hiring Manager Outreach**:
   - Automatically generates cold email pitches and 280-character LinkedIn connection notes.

8. **👑 Built-In Admin Console**:
   - Live registered user table, analysis history logs, and 1-click usage credit management.

---

## 🛠️ Architecture & Tech Stack

```text
[ Web Interface ]          [ Server API & Auth ]        [ AI Core Service Engine ]      [ Managed Models ]
• Dark Glassmorphism   --> • User Authentication   -->  • Multi-Provider Routing   -->  • Gemini 2.5 Flash
• Top Navigation Tabs      • SQLite Database           • Exponential Backoff           • OpenRouter Models
• Real Stats Engine        • Monthly Credit Limit      • Deterministic Cache           • OpenAI GPT
```

---

## 🚀 Quickstart & Installation

### 1. Clone Repository & Setup Environment
```bash
git clone https://github.com/Ankushh0027/Resume-Analyser.git
cd Resume-Analyser
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory:
```env
# Server-Side Managed AI Credentials
GEMINI_API_KEY=your_google_gemini_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
OPENAI_API_KEY=your_openai_api_key

# Platform Configuration
MAX_RETRIES=3
RATE_LIMIT_RPM=15
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Application
```bash
streamlit run app.py
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.
