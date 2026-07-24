# AI Resume Analyzer ⚡ (v2.5 Platform Build)

[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)](https://streamlit.io/)
[![Google Gemini API](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-4285F4.svg)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**AI Resume Analyzer** is an enterprise-grade, portfolio-defining SaaS platform engineered with **Python 3.13**, **Streamlit**, and **Google Gemini 2.5 Flash**. It provides candidates and tech professionals with a complete 360° suite of resume tools—from ATS Resume Scoring and Cover Letter Generation to Recruiter Cold Email Crafting and Market Salary Estimation.

---

## 🚀 7 Core Resume Engineering Modules

```
                        +---------------------------------------+
                        |   Streamlit SaaS Navigation Sidebar   |
                        |              (app.py)                 |
                        +-------------------+-------------------+
                                            |
    +-------------+-------------+-----------+-----------+-------------+-------------+
    |             |             |           |           |             |             |
    v             v             v           v           v             v             v
+-------+     +-------+     +-------+   +-------+   +-------+     +-------+     +-------+
| 📊 ATS|     | 📝 CV |     | ⚡ Bullet|  | 🆚 A/B|   | 🎯 Mock|    | 📧 Cold|     | 💼 Pay|
|Analyze|     | Cover |     |Enhance|   | Test  |   |Predict|     | Email |     |  Est  |
+-------+     +-------+     +-------+   +-------+   +-------+     +-------+     +-------+
```

### 1. 📊 AI Resume Analyzer & JD Matcher
- **100-Point ATS Scoring Rubric**: Itemized category breakdown (Formatting, Hard Skills, Quantifiable Metrics, Experience Fit).
- **Skill Taxonomy Extraction**: Technical Skills, Soft Skills, and Missing Industry Skills.
- **Job Description Matcher**: Calculates targeted JD Match Score %, extracts matching keywords, and highlights missing keywords.

### 2. 📝 AI Tailored Cover Letter Generator
- Generates a customized, professional 3-paragraph cover letter tailored to the candidate's resume and target Job Description.
- Features 1-click **Download Cover Letter (.txt)** and key highlights summary.

### 3. ⚡ AI Bullet Point Enhancer & Action Verb Rewriter
- Transforms weak, passive bullet points (*"Worked on API bugs"*) into high-impact, quantified achievements using the Google XYZ resume formula (*"Architected high-throughput FastAPI microservices processing 2.5M+ requests daily"*).

### 4. 🆚 Side-by-Side Resume A/B Comparison
- Upload 2 versions of a resume (Version A vs Version B) to compare ATS Scores, Technical Skill Counts, and Executive Summaries side-by-side to identify the winning version.

### 5. 🎯 AI Resume Interview Question Predictor
- Predicts 10 targeted Technical & STAR Behavioral interview questions based on the candidate's resume and target Job Description.

### 6. 📧 Recruiter Cold Email & LinkedIn Outreach Generator
- Crafts personalized cold emails for recruiters, direct hiring manager outreach messages, and short LinkedIn connection notes (< 280 chars).

### 7. 💼 Market Salary Range & Readiness Estimator
- Calculates base market compensation ranges (Min, Median, Max USD), identifies value-driving technical skills, and lists salary negotiation leverage points.

---

## 🛠️ Architecture & Tech Stack

- **Language**: Python 3.13
- **Frontend / Dashboard**: Streamlit (Glassmorphic Theme + Custom CSS + HTML5 Flow-Field Canvas)
- **AI Engine**: Google Gemini 2.5 Flash (`google-generativeai`)
- **Document Parsing**: `pdfplumber`, `python-docx`
- **Caching & Reliability**: MD5 Content Hash Caching, 3s Exponential Backoff Auto-Retry, Multi-Model Fallbacks

---

## 📁 Repository Directory Layout

```text
Resume-Analysis/
│── app.py                 # Multi-module Streamlit dashboard application
│── requirements.txt       # Project dependencies
│── README.md              # Documentation
│── .gitignore             # Git exclusion rules
│── .env.example           # Environment template
│── assets/
│   └── logo.svg           # Vector SVG brand logo
│── components/ui/         # React / shadcn flow-field component primitives
│   ├── flow-field-background.tsx
│   └── demo.tsx
│── tests/                 # Unit test suite
└── src/
    │── __init__.py        # Package initialization
    │── config.py          # Centralized configuration dataclass
    │── logger.py          # Formatted logging pipeline
    │── utils.py           # Text cleaning, sample loader, & report generators
    │── parser.py          # PDF & DOCX text extraction
    │── prompts.py         # System instructions & structured prompt templates
    │── llm.py             # Gemini API client wrapper with model fallbacks
    └── analyzer.py        # Service orchestrator facade
```

---

## 🚀 Quickstart Guide

### 1. Clone Repository & Setup Virtual Environment
```bash
git clone https://github.com/Ankushh0027/Resume-Analyser.git
cd Resume-Analyser

python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up API Key (`.env`)
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
LOG_LEVEL=INFO
```
*(Get a free API key at [Google AI Studio](https://aistudio.google.com/))*

### 4. Run the Resume Suite Dashboard
```bash
streamlit run app.py
```

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for details.
