# AI Resume Analyzer & Career Intelligence Suite ⚡

[![Live App](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](https://resume-analyser-ankush.streamlit.app/)
[![Python Version](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![AI Engine](https://img.shields.io/badge/Multi--Provider-Gemini%20%7C%20OpenRouter%20%7C%20OpenAI-4285F4.svg?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Database](https://img.shields.io/badge/Database-SQLite%203-003B57.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

An enterprise-grade, open-source platform for **AI Resume Auditing, Regional Salary Estimations, Cover Letter Generation, Bullet Rewriting, Recruiter Outreach, and Mock Interview Scenario Prediction**.

Inspired by top career platforms (Rezi AI, Grammarly, and ChatGPT), this codebase is designed with a **Dark Glassmorphic UI**, **Zero-User-API-Key Management**, and a **Resilient Multi-Provider LLM Engine**.

---

## 🌐 Live Application & Demo Account

- **Live Application Link**: [https://resume-analyser-ankush.streamlit.app/](https://resume-analyser-ankush.streamlit.app/)
- **Instant Demo Account**: Click **`⚡ Continue with Instant Demo Account`** on the login screen to evaluate sample resumes immediately without registration.

---

## 🌟 Comprehensive Feature Suite

### 1. 📊 ATS Compatibility Engine & Dashboard
- **4 Core Rubrics**: Evaluates **Formatting (20 pts)**, **Technical Stack (30 pts)**, **Quantifiable Impact Metrics (30 pts)**, and **Experience Fit (20 pts)**.
- **Deterministic Hashing**: Implements MD5 content hashing so identical resumes yield identical scores every time.
- **Deep Skill Extraction**: Automatically identifies technical skills, soft skills, missing skills, strengths, weaknesses, and pre-application checklist items.

### 2. 💼 Region & Company-Tier Adjusted Salary Engine
- **Multi-Country Support**: Calculates realistic compensation across **India (INR ₹ LPA)**, **United States ($ USD)**, **United Kingdom (£ GBP)**, **European Union (€ EUR)**, **Canada**, **Australia**, and **Global Remote**.
- **Tier-Adjusted Pay Scales**: Accounts for equity, RSUs, performance bonuses, and tier adjustments across **Tier 1 FAANG / Global Tech**, **Unicorn Scaleups**, **MNC Enterprises**, **Early-Stage Startups**, and **Consulting Agencies**.

### 3. 📝 Executive Cover Letter Generator
- Generates 3-paragraph executive cover letters matching the candidate's background against target job descriptions with 1-click `.txt` download.

### 4. ⚡ STAR Bullet Point Enhancer
- Transforms weak resume bullet points into high-impact, STAR-formatted statements enriched with strong action verbs and quantifiable metrics.

### 5. 🆚 Resume A/B Version Comparator
- Evaluates two resume versions side-by-side to display ATS score deltas, added technical skills, and improvements.

### 6. 🎯 Mock Interview Question Predictor
- Predicts role-specific technical deep-dive questions and STAR behavioral interview scenarios.

### 7. 📧 Recruiter & Hiring Manager Outreach Generator
- Generates high-converting cold recruiter emails, hiring manager emails, and 280-character LinkedIn connection notes.

### 8. 👑 Built-In SQLite Admin Console
- Accessible to authorized admin emails (`ankush@gmail.com`, `admin@resumeai.com`). Features a live user table, credit counts, and 1-click usage reset tools.

---

## 🏗️ Technical Architecture & How It Works

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           ARCHITECTURE OVERVIEW                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

   ┌───────────────────────────┐         ┌───────────────────────────┐
   │    User Browser / UI      │         │   Authentication Wall     │
   │  (Streamlit + Glassmorphism) ◄──────►│    (src/auth.py + SHA-256)│
   └─────────────┬─────────────┘         └─────────────┬─────────────┘
                 │                                     │
                 ▼                                     ▼
   ┌───────────────────────────┐         ┌───────────────────────────┐
   │    Document Parser        │         │    SQLite Database        │
   │  (pdfplumber + docx)      │         │(data/saas_resume_analyzer)│
   └─────────────┬─────────────┘         └─────────────┬─────────────┘
                 │                                     │
                 ▼                                     ▼
   ┌─────────────────────────────────────────────────────────────────┐
   │                  AI Service Engine Manager                      │
   │              (src/services/ai_service.py)                       │
   │   • MD5 Content Hash Determinism    • Retry Engine (Backoff)    │
   │   • Universal Skill Extractor       • Global Error Masking      │
   └───────────────────────────────┬─────────────────────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
 ┌───────────────┐         ┌───────────────┐         ┌───────────────┐
 │ Gemini 2.5    │         │ OpenRouter    │         │ OpenAI GPT    │
 │ (Primary API) │ ──────► │ (Fallback #1) │ ──────► │ (Fallback #2) │
 └───────────────┘         └───────────────┘         └───────────────┘
```

### 1. Document Parsing Pipeline (`src/parser.py`)
- **PDF Extraction**: Primary parsing via `pdfplumber` with automatic fallback to `PyPDF2` for complex vector or tabular PDFs.
- **DOCX Extraction**: Extracts text from both main document paragraphs and nested table cells (`doc.tables`).

### 2. Multi-Provider Managed AI Architecture (`src/services/ai_service.py` & `src/providers/`)
- All LLM API calls execute server-side with zero user key entry required.
- **Primary Routing**: Requests are sent to **Google Gemini 2.5 Flash**.
- **Automatic Fallback**: If rate limits occur, requests fall back seamlessly to **OpenRouter Free Models** and **OpenAI GPT-4o-mini**.
- **Exponential Backoff**: Executes automatic retries with exponential delays (2s ➔ 5s ➔ 10s).

### 3. Database & Auth Layer (`src/database.py` & `src/auth.py`)
- **SQLite Engine**: Physical database stored at `data/saas_resume_analyzer.db`.
- **Tables**:
  - `users`: Stores User ID, Name, Email, SHA-256 Password Hash, Creation Timestamp.
  - `usage_limits`: Tracks monthly analysis count (3 free analyses per account).
  - `analysis_history`: Stores complete JSON payloads, extracted text, and ATS scores for past audits.

---

## 📂 Project Directory Structure

```text
Resume-Analyser/
├── app.py                      # Main Streamlit web application & top tab layout
├── requirements.txt            # Python package dependencies
├── README.md                   # Project documentation & fork guide
├── .env.example                # Template for environment variables
├── data/
│   └── saas_resume_analyzer.db # Persistent SQLite database
├── src/
│   ├── analyzer.py             # Core facade for analysis, salary, and outreach
│   ├── auth.py                 # User login, registration wall & session auth
│   ├── config.py               # Managed API key and environment config
│   ├── database.py             # SQLite helper functions, schema & queries
│   ├── llm.py                  # LLM service orchestration & provider fallbacks
│   ├── parser.py               # PDF and DOCX document extraction engine
│   ├── prompts.py              # System prompts for ATS scoring & salary estimation
│   ├── providers/
│   │   ├── base.py             # Abstract base provider interface
│   │   ├── gemini_provider.py  # Google Gemini 2.5 Flash implementation
│   │   ├── mock_provider.py    # Offline fallback provider for testing
│   │   ├── openai_provider.py  # OpenAI GPT model implementation
│   │   └── openrouter_provider.py # OpenRouter multi-model implementation
│   └── services/
│       ├── ai_service.py       # Result sanitization & skill list resolver
│       └── usage_service.py    # Free tier credit limit enforcement
└── tests/
    ├── test_analyzer.py        # Unit tests for document analyzer
    └── test_saas_features.py   # Integration tests for auth and limits
```

---

## 🍴 How to Fork & Run Locally

If you want to fork this project and customize it for your own team or portfolio:

### Step 1: Fork & Clone Repository
Click the **Fork** button at the top right of this GitHub page, then clone your fork:
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/Resume-Analyser.git
cd Resume-Analyser
```

### Step 2: Configure Environment Variables
Create a `.env` file in the root folder:
```env
# Server-Side Managed AI Credentials
GEMINI_API_KEY=your_google_gemini_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
OPENAI_API_KEY=your_openai_api_key

# Execution Configuration
MAX_RETRIES=3
RATE_LIMIT_RPM=15
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Application
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.

