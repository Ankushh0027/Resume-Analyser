# AI Resume Analyzer ⚡ (v2.5 Production Build)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-FF4B4B.svg?style=for-the-badge&logo=streamlit)](https://resume-analyser.streamlit.app)
[![Python Version](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![AI Engine](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-4285F4.svg?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

An enterprise-grade, portfolio-defining **AI Resume Analyzer & Intelligence SaaS Platform** built with **Python 3.13**, **Streamlit**, and **Google Gemini 2.5 Flash**.

This repository is designed for developers, job seekers, and recruiters. Anyone can fork this project to deploy their own AI-powered career assistant or extend its features.

🌐 **Live Web Application**: [https://resume-analyser.streamlit.app](https://resume-analyser.streamlit.app)

---

## 📐 System Design & Architecture Overview

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

### 🧠 Core Architectural Pillars

1. **Facade Pattern (`src/analyzer.py`)**: Unified entrypoint orchestrating parsing, caching, prompt generation, and LLM requests.
2. **Resilient Multi-Model Fallback Chain (`src/llm.py`)**: Automatically detects model availability (`404 NOT_FOUND`) and skips to fallback active tiers (`gemini-2.5-flash` ➔ `gemini-2.0-flash` ➔ `gemini-1.5-flash-latest`).
3. **Automated Exponential Backoff on 429 Limits**: Prevents rate limit quota crashes by applying a 3-second delay loop before retrying.
4. **MD5 Content Hash Caching (`_ANALYSIS_CACHE`)**: Identical resume uploads serve cached JSON responses instantly with 0 API token consumption.
5. **100% In-Memory Document Processing**: File buffers process in RAM without persisting user resumes to disk for privacy guarantee.

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
