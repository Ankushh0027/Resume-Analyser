# AI Resume Analyzer ⚡ (v2.5 Production Build)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-FF4B4B.svg?style=for-the-badge&logo=streamlit)](https://resume-analyser.streamlit.app)
[![Python Version](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![AI Engine](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-4285F4.svg?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

An enterprise-grade, portfolio-defining **AI Resume Analyzer & Intelligence SaaS Platform** built with **Python 3.13**, **Streamlit**, and **Google Gemini 2.5 Flash**.

This repository showcases production-ready **Generative AI Engineering, LLM System Architecture, Prompt Engineering, and Full-Stack Python Application Development**.

🌐 **Live Web Application**: [https://resume-analyser.streamlit.app](https://resume-analyser.streamlit.app)

---

## 🛠️ Comprehensive Tech Stack & AI Competencies

```
                     +-------------------------------------------------------+
                     |           TECHNOLOGY STACK & AI ARCHITECTURE          |
                     +-------------------------------------------------------+

   [ Generative AI & LLMs ]            [ Software Architecture ]            [ Frontend & UI ]
   • Google Gemini 2.5 Flash           • Facade Design Pattern              • Streamlit SaaS Framework
   • Chain-of-Thought (CoT)            • Multi-Model Fallback Chain         • Dark Glassmorphic Styling
   • Strict JSON Schema Output         • 429 Exponential Backoff            • HTML5 Canvas Flow Field API
   • Google XYZ Formula Rewriting      • MD5 Content Hash Caching           • React & TypeScript Primitives

   [ Document Processing ]             [ Quality & Security ]               [ Cloud & DevOps ]
   • pdfplumber (PDF Extract)          • 100% In-Memory Parsing             • Git & GitHub Version Control
   • python-docx (DOCX Extract)        • Unit Testing (unittest.mock)       • Streamlit Community Cloud
   • Structured RegEx Cleaning         • Custom Exception Hierarchy         • Encrypted Secrets Storage
```

### 🤖 1. Artificial Intelligence & LLM Engineering
- **LLM Providers & Models**: Google Gemini 2.5 Flash, Gemini 2.0 Flash, Gemini 1.5 Flash (`google-generativeai`).
- **Prompt Engineering**: Chain-of-Thought (CoT) reasoning, System Instructions, strict JSON response schema enforcement, Google XYZ Resume Rewriting Formula.
- **AI Resilience & Fault Tolerance**: Multi-model fallback execution, 404 endpoint skipping, 3s exponential backoff auto-retry for 429 rate limit spikes.
- **In-Memory Caching**: MD5 Content Hashing (`_ANALYSIS_CACHE`) to bypass redundant LLM API calls and save tokens.

### 🐍 2. Backend & System Architecture
- **Language**: Python 3.13 (Type Annotations, Dataclasses, Custom Exception Handling).
- **Design Patterns**: Service Orchestrator Facade (`ResumeAnalyzer`), Lazy Client Instantiation (`get_analyzer()`), Modular Package Architecture.
- **Document Parsing**: `pdfplumber` (PDF layout & text extraction), `python-docx` (DOCX parsing).
- **Quality Assurance**: Unit Testing (`unittest`, `unittest.mock`), Logging Pipeline (`src/logger.py`).

### 🎨 3. Frontend & UI Engineering
- **Framework**: Streamlit (Session State Management, Radio Navigation, File Uploader).
- **Design System**: Dark Glassmorphism, Google Fonts (`Plus Jakarta Sans`), Neon Radial Glow Score Gauges.
- **Interactive Graphics**: HTML5 Canvas JavaScript API (500 Particle Flow Field Animation with mouse repulsion).
- **UI Components**: React & TypeScript primitives (`components/ui/flow-field-background.tsx`).

### ☁️ 4. Cloud Infrastructure & DevOps
- **Deployment**: Streamlit Community Cloud.
- **Secrets Management**: Secure API key handling via `st.secrets` & `.env` environment variables.
- **Version Control**: Git & GitHub Repository ([`Ankushh0027/Resume-Analyser`](https://github.com/Ankushh0027/Resume-Analyser)).

---

## 📐 System Architecture Diagram

```
                      +---------------------------------------+
                      |       Streamlit SaaS Web UI           |
                      |              (app.py)                 |
                      +-------------------+-------------------+
                                          |
                      +-------------------+-------------------+
                      |   ResumeAnalyzer Orchestrator Facade  |
                      |            (src/analyzer.py)          |
                      +---------+-------------------+---------+
                                |                   |
                                v                   v
                     +--------------------+  +--------------------+
                     |    Parser Engine   |  |   MD5 Content Hash |
                     | (pdfplumber/docx)  |  |    Cache Store     |
                     +--------------------+  +--------------------+
                                                    |
                                                    v
                                         +--------------------+
                                         | Gemini API Client  |
                                         |    (src/llm.py)    |
                                         +---------+----------+
                                                   |
                     +-----------------------------+-----------------------------+
                     |                             |                             |
                     v                             v                             v
           +-------------------+         +-------------------+         +-------------------+
           | Primary Model:    | (404/   | Secondary Model:  | (404/   | Fallback Model:   |
           | gemini-2.5-flash  |  429)   | gemini-2.0-flash  |  429)   | gemini-1.5-flash  |
           +-------------------+ ------> +-------------------+ ------> +-------------------+
```

---

## 🚀 7 Core Resume Suite Modules

| Module | Icon | Description |
| :--- | :---: | :--- |
| **ATS Resume Analyzer** | 📊 | 100-point rubric audit (Formatting, Tech Skills, Metrics, Fit) with skill taxonomy. |
| **Tailored Cover Letter** | 📝 | Generates customized 3-paragraph executive cover letters from target JDs. |
| **Google XYZ Bullet Rewriter** | ⚡ | Rewrites weak bullets into quantified metric achievement statements. |
| **Side-by-Side A/B Tester** | 🆚 | Upload 2 resume versions to compare ATS scores & skills side-by-side. |
| **AI Mock Interview Predictor** | 🎯 | Predicts 10 targeted Technical & STAR Behavioral interview questions. |
| **Recruiter Outreach Generator** | 📧 | Cold emails for recruiters, hiring manager pitches & LinkedIn notes (< 280 chars). |
| **Salary Range Estimator** | 💼 | Market base salary range estimator (USD), value skills & negotiation leverage points. |

---

## 📁 Repository Directory Layout

```text
Resume-Analysis/
│── app.py                 # Streamlit web application dashboard entrypoint
│── requirements.txt       # Dependencies
│── README.md              # Project documentation
│── .gitignore             # Git rules
│── .env.example           # Environment template
│── .streamlit/
│   └── config.toml        # Production UI theme configuration
│── assets/
│   └── logo.svg           # Product SVG branding logo
│── components/ui/         # React / shadcn background primitives
│   ├── flow-field-background.tsx
│   └── demo.tsx
│── tests/                 # Unit test suite
│   ├── test_analyzer.py
│   └── test_llm.py
└── src/
    │── __init__.py        # Package initialization
    │── config.py          # Configuration dataclass
    │── logger.py          # Formatted logging pipeline
    │── utils.py           # Text cleaning, report generation & sample loader
    │── parser.py          # PDF & DOCX text extraction
    │── prompts.py         # System instructions & JSON prompt builders
    │── llm.py             # Gemini API client wrapper with resilience chain
    └── analyzer.py        # Service orchestrator facade
```

---

## 🛠️ Quickstart & Local Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/Ankushh0027/Resume-Analyser.git
cd Resume-Analyser
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (`.env`)
Create a `.env` file in the root folder:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
LOG_LEVEL=INFO
```
*(Get a free API key at [Google AI Studio](https://aistudio.google.com/))*

### 5. Launch the Streamlit App
```bash
streamlit run app.py
```

---

## ☁️ How to Fork & Deploy to Streamlit Cloud

1. **Fork this repository** on GitHub.
2. Sign in to **[share.streamlit.io](https://share.streamlit.io/)** with GitHub.
3. Click **New app** and select your forked repository.
4. Set Main file path to `app.py`.
5. In **Advanced Settings -> Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```
6. Click **Deploy!** 🚀

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for details.
