# AI Resume Analyzer & Career Intelligence Suite ⚡

[![Live App](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](https://www.resume-analyser-app-xyqm7i.streamlit.app/)
[![Python Version](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![AI Engine](https://img.shields.io/badge/Multi--Provider-Gemini%20%7C%20OpenRouter%20%7C%20OpenAI-4285F4.svg?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Database](https://img.shields.io/badge/Database-Supabase%20PostgreSQL-3ECF8E.svg?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

An enterprise-grade, open-source platform for **AI Resume Auditing, Regional Salary Estimations, Cover Letter Generation, STAR Bullet Point Rewriting, Recruiter Outreach, Mock Interview Scenario Prediction, and Live Sponsor Ad Management**.

Inspired by top career platforms (Rezi AI, Grammarly, and ChatGPT), this platform is engineered with a **Dark Glassmorphic UI**, **Zero-User-API-Key Management**, **Supabase PostgreSQL Cloud DB**, **Forgot Password Engine**, and a **Resilient Multi-Provider LLM Architecture**.

---

## 🌐 Live Application & Instant Access

- **Live App Link**: [https://www.resume-analyser-app-xyqm7i.streamlit.app/](https://www.resume-analyser-app-xyqm7i.streamlit.app/)
- **Instant Demo Account**: Click **`⚡ Continue with Instant Demo Account`** on the login screen to evaluate sample resumes immediately without registration.
- **Support & Inquiries**: `autoflowai06@gmail.com`

---

## 🌟 Comprehensive Feature Suite

### 1. 📊 ATS Compatibility Engine & Dashboard
- **4 Core Rubrics**: Evaluates **Formatting (20 pts)**, **Technical Stack (30 pts)**, **Quantifiable Impact Metrics (30 pts)**, and **Experience Fit (20 pts)**.
- **Deterministic Hashing**: Implements MD5 content hashing so identical resumes yield identical scores every time.
- **Deep Skill & Insight Badges**: Automatically extracts technical skills, soft skills, missing skills, strengths, weaknesses, and pre-application checklist items into styled UI badges.

### 2. 💼 Region & Company-Tier Adjusted Salary Engine
- **Multi-Country Support**: Calculates realistic compensation across **India (INR ₹ LPA)**, **United States ($ USD)**, **United Kingdom (£ GBP)**, **European Union (€ EUR)**, **Canada**, **Australia**, and **Global Remote**.
- **Tier-Adjusted Pay Scales**: Accounts for equity, RSUs, performance bonuses, and tier adjustments across **Tier 1 FAANG / Global Tech**, **Unicorn Scaleups**, **MNC Enterprises**, **Early-Stage Startups**, and **Consulting Agencies**.

### 3. 🔒 Authentication & Account Recovery Portal
- **3-Tab Authentication Hub**: Supports **🔑 Log In**, **✨ Create Account**, and **🔒 Forgot Password**.
- **Password Reset Engine**: Allows registered users to reset their account password securely with SHA-256 encryption.
- **Session Persistence**: Maintains user state cleanly across app navigations.

### 4. 📝 Executive Cover Letter Generator
- Generates 3-paragraph executive cover letters matching the candidate's background against target job descriptions with 1-click `.txt` download.

### 5. ⚡ STAR Bullet Point Enhancer
- Transforms weak resume bullet points into high-impact, STAR-formatted statements enriched with strong action verbs and quantifiable metrics.

### 6. 🆚 Resume A/B Version Comparator
- Evaluates two resume versions side-by-side to display ATS score deltas, added technical skills, and improvements.

### 7. 🎯 Mock Interview Scenario Predictor
- Predicts role-specific technical deep-dive questions and STAR behavioral interview scenarios.

### 8. 📧 Recruiter & Hiring Manager Outreach Generator
- Generates high-converting cold recruiter emails, hiring manager emails, and 280-character LinkedIn connection notes.

### 9. 📢 Live Sponsor Ad Management Engine
- Allows platform admins to toggle live banner advertisements, customize ad headlines, description text, badge tags, and destination links directly via the Admin Panel.

### 10. 👑 Admin Console & Cloud Analytics
- Accessible to authorized admins (`autoflowai06@gmail.com`). Features a live user database, system audit statistics, real-time database connection status (`Supabase PostgreSQL SSL`), and usage reset tools.

---

## 🏗️ Technical Architecture & How It Works

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           ARCHITECTURE OVERVIEW                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

   ┌───────────────────────────┐         ┌───────────────────────────┐
   │    User Browser / UI      │         │   Authentication Hub      │
   │  (Streamlit + Glassmorphic) ◄──────►│   (Auth, Signup, Password)│
   └─────────────┬─────────────┘         └─────────────┬─────────────┘
                 │                                     │
                 ▼                                     ▼
   ┌───────────────────────────┐         ┌───────────────────────────┐
   │    Document Parser        │         │ Supabase PostgreSQL DB    │
   │  (pdfplumber + docx)      │         │(Pooler SSL / SQLite Fallback)│
   └─────────────┬─────────────┘         └─────────────┬─────────────┘
                 │                                     │
                 ▼                                     ▼
   ┌─────────────────────────────────────────────────────────────────┐
   │                  AI Service Engine Manager                      │
   │              (src/services/ai_service.py)                       │
   │   • MD5 Content Hash Determinism    • Retry Engine (Backoff)    │
   │   • Universal Skill Extractor       • Global Error Masking      │
   └─────────────┬───────────────────────────────────────────────────┘
                 │
         ┌───────┼─────────────────────────┐
         ▼       ▼                         ▼
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

### 3. Persistent Database & Security Layer (`src/database.py` & `src/auth.py`)
- **Cloud Engine**: Supabase PostgreSQL DB via Transaction Pooler (`sslmode=require`).
- **Local Fallback**: SQLite fallback (`data/saas_resume_analyzer.db`).
- **Tables**:
  - `users`: User ID, Name, Email, SHA-256 Password Hash, Registration Timestamp.
  - `usage_limits`: Monthly analysis count, plan tier, and extra credits per account.
  - `analysis_history`: Stores full JSON audit payloads, extracted text, and ATS scores for past evaluations.

---

## 📂 Project Directory Structure

```text
Resume-Analyser/
├── app.py                      # Main Streamlit web application & top tab layout
├── requirements.txt            # Python package dependencies
├── README.md                   # Project documentation
├── .env.example                # Template for environment variables
├── data/
│   └── saas_resume_analyzer.db # Local SQLite database fallback
├── scripts/
│   └── test_supabase_conn.py   # Supabase connection verification utility
├── src/
│   ├── ads.py                  # Sponsor Ad Management & Banner Engine
│   ├── analyzer.py             # Core facade for ATS scoring, salary, and outreach
│   ├── auth.py                 # User login, signup, password reset & auth header
│   ├── config.py               # Managed API key and environment config
│   ├── database.py             # Supabase PostgreSQL / SQLite database engine
│   ├── llm.py                  # LLM service orchestration & provider fallbacks
│   ├── parser.py               # PDF and DOCX document extraction engine
│   ├── payments.py             # Payment order utilities
│   ├── prompts.py              # System prompts for ATS scoring & salary estimation
│   ├── providers/
│   │   ├── base.py             # Abstract base provider interface
│   │   ├── gemini_provider.py  # Google Gemini 2.5 Flash implementation
│   │   ├── mock_provider.py    # Offline fallback provider for testing
│   │   ├── openai_provider.py  # OpenAI GPT model implementation
│   │   └── openrouter_provider.py # OpenRouter multi-model implementation
│   └── services/
│       ├── ai_service.py       # Result sanitization & skill list resolver
│       └── usage_service.py    # Usage limit management
└── tests/
    ├── test_analyzer.py        # Unit tests for document analyzer
    └── test_saas_features.py   # Integration tests for auth and database
```

---

## 🍴 How to Run Locally & Setup Supabase

### Step 1: Clone Repository
```bash
git clone https://github.com/Ankushh0027/Resume-Analyser.git
cd Resume-Analyser
```

### Step 2: Configure `.env` File
Create a `.env` file in the project root:

```env
# Supabase PostgreSQL Connection String (Transaction Pooler)
DATABASE_URL=postgresql://postgres.emkarnsfdneiqgmbnvit:resume9878635@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres

# Managed AI Credentials
GEMINI_API_KEY=your_google_gemini_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
OPENAI_API_KEY=your_openai_api_key

# Execution Controls
MAX_RETRIES=3
RATE_LIMIT_RPM=15
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Launch Application
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
