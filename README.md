# AI Resume Analyzer ⚡

[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)](https://streamlit.io/)
[![Google Gemini API](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-4285F4.svg)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-grade, portfolio-quality **AI Resume Analyzer** built with **Python 3.13**, **Streamlit**, and the **Google Gemini API**. 

The application enables job applicants and recruiters to upload resumes in **PDF** or **DOCX** format and receive instant, structured AI evaluation, including ATS compatibility scoring, skill gap detection, strengths/weaknesses identification, and actionable feedback.

---

## 🏛️ System Architecture

The application follows clean software architecture principles, strictly separating presentation (Streamlit UI), domain orchestration (Facade pattern), document parsing, and LLM prompt engineering.

```
                        +-------------------------+
                        |     Streamlit UI        |
                        |       app.py            |
                        +------------+------------+
                                     |
                                     v
                        +-------------------------+
                        |    Resume Analyzer      |
                        |    src/analyzer.py      |
                        +------+-----------+------+
                               |           |
                 +-------------+           +-------------+
                 |                                       |
                 v                                       v
      +------------------------+             +--------------------------+
      |    Resume Parser       |             |      Gemini Client       |
      |    src/parser.py       |             |       src/llm.py         |
      | pdfplumber/python-docx |             +------------+-------------+
      +------------+-----------+                          |
                   |                                      |
                   |                                      v
                   |                         +--------------------------+
                   |                         |      Prompt Builder      |
                   |                         |     src/prompts.py       |
                   |                         +--------------------------+
                   |
                   v
      +------------------------+
      |      Config            |
      |     src/config.py      |
      +------------------------+
```

---

## ✨ Features

- **Document Ingestion**: Multi-format support for `.pdf` (using `pdfplumber`) and `.docx` (using `python-docx`).
- **ATS Compatibility Score**: Calculates an overall rating (0–100) based on structure, keyword density, and clarity.
- **Skill Extraction & Taxonomy**:
  - **Technical Skills**: Hard skills, languages, frameworks, tools.
  - **Soft Skills**: Leadership, communication, collaboration.
  - **Missing Skills**: Key industry-standard competencies missing for the target role.
- **Executive Summary**: 3–4 sentence profile evaluation.
- **SWOT Analysis**: Identifies top candidate strengths and areas of weakness.
- **Actionable Recommendations**: Numbered, step-by-step guidance for resume improvement.

---

## 🛠️ Tech Stack

- **Language**: Python 3.13
- **Frontend / Dashboard**: Streamlit
- **LLM / AI Model**: Google Gemini 2.5 Flash (`google-generativeai`)
- **Document Parsing**: `pdfplumber`, `python-docx`
- **Environment Management**: `python-dotenv`
- **Logging & Validation**: Python standard `logging`, `pydantic`

---

## 📁 Directory Structure

```text
AI-Resume-Analyzer/
│── app.py                 # Streamlit dashboard interface
│── requirements.txt       # Project dependencies
│── README.md              # Project documentation
│── .gitignore             # Git ignore rules
│── .env.example           # Environment template
│── assets/                # Visual assets & badges
│── data/                  # Sample datasets & schemas
│── docs/                  # Architectural notes
│── models/                # Local data models
│── tests/                 # Unit test suite
│── uploads/               # Temporary file directory
└── src/
    │── __init__.py        # Package initialization
    │── config.py          # Configuration manager
    │── logger.py          # Centralized logging setup
    │── utils.py           # Text cleaning & validation helpers
    │── parser.py          # PDF & DOCX text extraction
    │── prompts.py         # System instructions & JSON schemas
    │── llm.py             # Gemini API client wrapper
    │── analyzer.py        # Facade service orchestrator
```

---

## 🚀 Quickstart Guide

### 1. Clone Repository
```bash
git clone https://github.com/Ankushh0027/Resume-Analyser.git
cd Resume-Analyser
```

### 2. Set Up Virtual Environment
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

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and add your Gemini API key:
```bash
cp .env.example .env
```
Inside `.env`:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
LOG_LEVEL=INFO
```
*(Get a free API key at [Google AI Studio](https://aistudio.google.com/))*

### 5. Run the Application
```bash
streamlit run app.py
```

---

## 🧪 Running Unit Tests

Run the test suite using `unittest`:
```bash
python -m unittest discover -s tests
```

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for details.
