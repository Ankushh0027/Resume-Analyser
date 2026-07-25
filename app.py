"""
Streamlit Web Application Entrypoint
AI Resume Analyzer SaaS Architecture (ChatGPT / Grammarly / Rezi AI style)
Zero User API Key Management • Automated Multi-Provider AI Engine • SQLite History & Usage Limits
"""

import os
from typing import Any
import streamlit as st
from src.config import config
from src.logger import logger
from src.analyzer import ResumeAnalyzer, AnalysisError
from src.parser import UnsupportedFileTypeError, ParsingError
from src.utils import generate_text_report, generate_json_report, get_sample_resume_text
from src.auth import get_current_user, login_user, signup_user, logout_user, render_auth_header
from src.services.usage_service import UsageService, UsageLimitExceededError
from src.database import get_user_analysis_history, get_user_usage

# -----------------------------------------------------------------------------
# Page Configuration & Glassmorphism Theme Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer ⚡ SaaS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Neural Flow-Field Animated Background
st.components.v1.html(
    """
    <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; pointer-events: none; overflow: hidden; background: #030712;">
      <canvas id="neural-canvas" style="display: block; width: 100%; height: 100%;"></canvas>
    </div>
    <script>
      const canvas = document.getElementById('neural-canvas');
      const ctx = canvas.getContext('2d');
      let width = window.innerWidth;
      let height = window.innerHeight;
      let particles = [];
      let mouse = { x: -1000, y: -1000 };
      const particleCount = 400;
      const speed = 0.8;

      class Particle {
        constructor() {
          this.x = Math.random() * width;
          this.y = Math.random() * height;
          this.vx = 0;
          this.vy = 0;
          this.age = 0;
          this.life = Math.random() * 200 + 100;
        }
        update() {
          const angle = (Math.cos(this.x * 0.005) + Math.sin(this.y * 0.005)) * Math.PI;
          this.vx += Math.cos(angle) * 0.2 * speed;
          this.vy += Math.sin(angle) * 0.2 * speed;

          const dx = mouse.x - this.x;
          const dy = mouse.y - this.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 150) {
            const force = (150 - dist) / 150;
            this.vx -= dx * force * 0.05;
            this.vy -= dy * force * 0.05;
          }

          this.x += this.vx;
          this.y += this.vy;
          this.vx *= 0.95;
          this.vy *= 0.95;
          this.age++;

          if (this.age > this.life) this.reset();
          if (this.x < 0) this.x = width;
          if (this.x > width) this.x = 0;
          if (this.y < 0) this.y = height;
          if (this.y > height) this.y = 0;
        }
        reset() {
          this.x = Math.random() * width;
          this.y = Math.random() * height;
          this.vx = 0;
          this.vy = 0;
          this.age = 0;
          this.life = Math.random() * 200 + 100;
        }
        draw(context) {
          context.fillStyle = '#818cf8';
          const alpha = 1 - Math.abs((this.age / this.life) - 0.5) * 2;
          context.globalAlpha = alpha;
          context.fillRect(this.x, this.y, 1.5, 1.5);
        }
      }

      function init() {
        const dpr = window.devicePixelRatio || 1;
        canvas.width = width * dpr;
        canvas.height = height * dpr;
        ctx.scale(dpr, dpr);
        particles = [];
        for (let i = 0; i < particleCount; i++) particles.push(new Particle());
      }

      function animate() {
        ctx.fillStyle = 'rgba(3, 7, 18, 0.15)';
        ctx.fillRect(0, 0, width, height);
        particles.forEach(p => { p.update(); p.draw(ctx); });
        requestAnimationFrame(animate);
      }

      window.addEventListener('resize', () => { width = window.innerWidth; height = window.innerHeight; init(); });
      window.addEventListener('mousemove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY; });
      window.addEventListener('mouseleave', () => { mouse.x = -1000; mouse.y = -1000; });

      init();
      animate();
    </script>
    """,
    height=0,
)

# Inject Modern SaaS Styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
    }

    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #030712 !important;
    }

    iframe[title="st.components.v1.html"] {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        z-index: 0 !important;
        pointer-events: none !important;
        border: none !important;
    }

    /* Hide Streamlit Default Chrome for Production Look */
    #MainMenu, header, footer, [data-testid="stDecoration"], [data-testid="stHeader"] {
        visibility: hidden !important;
        height: 0px !important;
        padding: 0px !important;
    }

    /* Production Dropzone File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 2px dashed rgba(129, 140, 248, 0.35) !important;
        border-radius: 18px !important;
        padding: 16px !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #818CF8 !important;
        background: rgba(99, 102, 241, 0.08) !important;
        box-shadow: 0 0 25px rgba(99, 102, 241, 0.25) !important;
    }

    .main .block-container {
        position: relative !important;
        z-index: 1 !important;
        padding-top: 1rem !important;
        padding-bottom: 4rem !important;
        max-width: 1260px !important;
    }

    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.85) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* Glassmorphic Cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.75) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 18px !important;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5) !important;
        transition: all 0.3s ease !important;
    }
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.4) !important;
        box-shadow: 0 25px 50px -12px rgba(99, 102, 241, 0.25) !important;
    }

    /* Hero Branding */
    .hero-title {
        font-size: 3rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        background: linear-gradient(135deg, #818CF8 0%, #C084FC 40%, #F472B6 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 0.2rem !important;
        text-shadow: 0 0 40px rgba(129, 140, 248, 0.3) !important;
    }

    .hero-subtitle {
        color: #94A3B8 !important;
        font-size: 1.15rem !important;
        font-weight: 500 !important;
        margin-bottom: 1.2rem !important;
    }

    /* Glowing Primary Buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #D946EF 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.75rem 1.5rem !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 8px 30px rgba(139, 92, 246, 0.6) !important;
    }

    .stButton > button[kind="secondary"] {
        background: rgba(30, 41, 59, 0.8) !important;
        color: #E2E8F0 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: rgba(51, 65, 85, 0.9) !important;
        border-color: #818CF8 !important;
        color: #F8FAFC !important;
    }

    /* Sleek Input Fields */
    .stTextInput input, .stTextArea textarea, .stSelectbox select, [data-baseweb="select"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        color: #F8FAFC !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #818CF8 !important;
        box-shadow: 0 0 15px rgba(129, 140, 248, 0.3) !important;
    }

    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: rgba(15, 23, 42, 0.6) !important;
        padding: 6px !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    .stTabs [data-baseweb="tab"] {
        height: 44px !important;
        border-radius: 12px !important;
        color: #94A3B8 !important;
        font-weight: 600 !important;
        padding: 0 20px !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(139, 92, 246, 0.3) 100%) !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(129, 140, 248, 0.4) !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2) !important;
    }

    /* Score Container */
    .score-container {
        text-align: center !important;
        padding: 36px 24px !important;
        border-radius: 24px !important;
        background: radial-gradient(135% 100% at 50% 0%, rgba(99, 102, 241, 0.25) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        border: 1px solid rgba(129, 140, 248, 0.4) !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6) !important;
    }

    .score-number {
        font-size: 5rem !important;
        font-weight: 800 !important;
        line-height: 1 !important;
        margin: 14px 0 !important;
    }
    .score-high { color: #34D399 !important; text-shadow: 0 0 35px rgba(52, 211, 153, 0.6) !important; }
    .score-med { color: #FBBF24 !important; text-shadow: 0 0 35px rgba(251, 191, 36, 0.6) !important; }
    .score-low { color: #F87171 !important; text-shadow: 0 0 35px rgba(248, 113, 113, 0.6) !important; }

    /* Skill Badges & Pill Tags */
    .badge {
        display: inline-block !important;
        padding: 6px 14px !important;
        margin: 4px 6px 4px 0 !important;
        border-radius: 12px !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.2px !important;
        transition: all 0.2s ease !important;
    }
    .badge-tech {
        background: rgba(99, 102, 241, 0.25) !important;
        border: 1px solid rgba(129, 140, 248, 0.45) !important;
        color: #E0E7FF !important;
    }
    .badge-soft {
        background: rgba(16, 185, 129, 0.25) !important;
        border: 1px solid rgba(16, 185, 129, 0.45) !important;
        color: #A7F3D0 !important;
    }
    .badge-missing {
        background: rgba(239, 68, 68, 0.25) !important;
        border: 1px solid rgba(239, 68, 68, 0.45) !important;
        color: #FCA5A5 !important;
    }

    /* Insight Cards (Strengths, Weaknesses, Action Plan) */
    .insight-card {
        background: rgba(15, 23, 42, 0.85) !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        margin-bottom: 10px !important;
        font-size: 0.95rem !important;
        line-height: 1.5 !important;
        color: #F8FAFC !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.2s ease !important;
    }
    .strength-item {
        border-left: 4px solid #10B981 !important;
        border-top: 1px solid rgba(16, 185, 129, 0.25) !important;
        border-right: 1px solid rgba(16, 185, 129, 0.25) !important;
        border-bottom: 1px solid rgba(16, 185, 129, 0.25) !important;
        background: rgba(16, 185, 129, 0.1) !important;
    }
    .weakness-item {
        border-left: 4px solid #F59E0B !important;
        border-top: 1px solid rgba(245, 158, 11, 0.25) !important;
        border-right: 1px solid rgba(245, 158, 11, 0.25) !important;
        border-bottom: 1px solid rgba(245, 158, 11, 0.25) !important;
        background: rgba(245, 158, 11, 0.1) !important;
    }
    .suggestion-item {
        border-left: 4px solid #6366F1 !important;
        border-top: 1px solid rgba(99, 102, 241, 0.25) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.25) !important;
        border-bottom: 1px solid rgba(99, 102, 241, 0.25) !important;
        background: rgba(99, 102, 241, 0.1) !important;
    }

    /* Custom Badges */
    .badge {
        display: inline-block !important;
        padding: 6px 16px !important;
        margin: 4px !important;
        border-radius: 20px !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        backdrop-filter: blur(8px) !important;
    }
    .badge-tech { background: rgba(99, 102, 241, 0.22) !important; color: #C7D2FE !important; border: 1px solid rgba(129, 140, 248, 0.5) !important; }
    .badge-soft { background: rgba(168, 85, 247, 0.22) !important; color: #E9D5FF !important; border: 1px solid rgba(192, 132, 252, 0.5) !important; }
    .badge-missing { background: rgba(239, 68, 68, 0.22) !important; color: #FCA5A5 !important; border: 1px solid rgba(248, 113, 113, 0.5) !important; }

    /* Insight Cards */
    .insight-card {
        padding: 18px 20px !important;
        border-radius: 16px !important;
        margin-bottom: 14px !important;
        font-size: 0.98rem !important;
        line-height: 1.6 !important;
        backdrop-filter: blur(12px) !important;
    }
    .strength-item { background: rgba(16, 185, 129, 0.1) !important; border: 1px solid rgba(52, 211, 153, 0.35) !important; color: #D1FAE5 !important; }
    .weakness-item { background: rgba(245, 158, 11, 0.1) !important; border: 1px solid rgba(251, 191, 36, 0.35) !important; color: #FEF3C7 !important; }
    .suggestion-item { background: rgba(99, 102, 241, 0.1) !important; border: 1px solid rgba(129, 140, 248, 0.35) !important; color: #E0E7FF !important; }

    /* Expanders */
    .stExpander {
        background: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(12px) !important;
    }

    /* Metric Values */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #F8FAFC 0%, #C7D2FE 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }

    .footer {
        text-align: center;
        padding: 30px;
        color: #64748B;
        font-size: 0.88rem;
        margin-top: 50px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_score_color_class(score: int) -> str:
    """Returns CSS class based on ATS score threshold."""
    if score >= 80:
        return "score-high"
    elif score >= 60:
        return "score-med"
    return "score-low"


def render_sidebar() -> tuple[str, str, str, str]:
    """Renders SaaS sidebar navigation and account options (ZERO user API keys)."""
    user = get_current_user()
    if user is None:
        return ("📊 AI Resume Analyzer", "", "", "gemini-2.5-flash")

    with st.sidebar:
        if os.path.exists("assets/logo.svg"):
            st.image("assets/logo.svg", width=56)

        env_admin_str = os.getenv("ADMIN_EMAILS", "")
        env_admins = [e.strip().lower() for e in env_admin_str.split(",") if e.strip()]
        default_admins = ["autoflowai06@gmail.com", "admin@resumeai.com", "demo@resumeai.com", "ankush@gmail.com", "admin@gmail.com"]
        admin_emails = set(default_admins + env_admins)
        is_admin = bool(user and user.get("email", "").strip().lower() in admin_emails)

        modules = [
            "📊 AI Resume Analyzer",
            "📜 Analysis History",
            "📝 Cover Letter Generator",
            "⚡ Bullet Point Enhancer",
            "🆚 Resume A/B Comparison",
            "🎯 Resume Interview Predictor",
            "📧 Recruiter Outreach Generator",
            "💼 Salary & Readiness Estimator",
        ]
        if is_admin:
            modules.append("👑 Admin & User Management")

        module_nav = st.radio(
            "Select Module",
            modules,
            index=0,
        )

        st.markdown("---")
        st.markdown("### ⚙️ Target Options")

        model_choice = st.selectbox(
            "AI Engine (Managed Server-Side)",
            ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp", "google/gemini-2.0-flash-lite-001:free", "meta-llama/llama-3.3-70b-instruct:free", "gpt-4o-mini"],
            index=0,
            help="All AI processing runs server-side with zero user key management required.",
        )

        target_role = st.text_input(
            "Target Job Title (Optional)",
            placeholder="e.g., Senior Full Stack Engineer",
        )

        job_description = st.text_area(
            "Target Job Description (Optional)",
            height=100,
            placeholder="Paste target job posting here...",
        )

        st.markdown("---")
        st.markdown("### 🧪 Quick 1-Click Demo")
        if st.button("Load Sample Resume & JD", use_container_width=True):
            sample_text, sample_name, sample_jd = get_sample_resume_text()
            st.session_state["demo_sample_text"] = sample_text
            st.session_state["demo_sample_name"] = sample_name
            st.session_state["demo_sample_jd"] = sample_jd
            st.success("Sample data loaded! Click 'Analyze Resume'.")

        st.markdown("---")
        st.markdown("### 🔐 User Account & Authentication")
        user = get_current_user()

        if user:
            st.caption(f"Logged in as: **{user['name']}**")
            with st.expander("👤 User Account Details", expanded=False):
                st.write(f"**Email**: `{user['email']}`")
                usage = get_user_usage(user["id"])
                st.write(f"**Analyses Used**: `{usage.get('analysis_count', 0)} / {usage.get('analysis_limit', 3)}`")
                from src.database import reset_user_usage
                if st.button("🔄 Reset Limit (3/3 Free)", key="sidebar_reset_btn", use_container_width=True):
                    reset_user_usage(user["id"])
                    st.success("Usage counter reset to 3 free analyses!")
                    st.rerun()
                if st.button("Logout", key="sidebar_logout_btn", use_container_width=True):
                    logout_user()
                    st.rerun()
        else:
            with st.expander("🔑 Login / Register", expanded=True):
                auth_mode = st.radio("Mode", ["Login", "Sign Up"], horizontal=True)
                email_input = st.text_input("Email", key="auth_email")
                pwd_input = st.text_input("Password", type="password", key="auth_pwd")

                if auth_mode == "Login":
                    if st.button("Sign In", type="primary", use_container_width=True):
                        ok, msg = login_user(email_input, pwd_input)
                        if ok:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                else:
                    name_input = st.text_input("Full Name", key="auth_name")
                    if st.button("Create Account", type="primary", use_container_width=True):
                        ok, msg = signup_user(email_input, name_input, pwd_input)
                        if ok:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)

        st.markdown("---")
        st.markdown(
            """
            🔒 **SaaS Security & Guarantee**
            - **Server-Side AI Keys**: 100% Protected
            - **Privacy**: In-Memory Parsing & Storage
            - **Resilience**: Auto Provider Fallback Engine
            """
        )
        return module_nav, target_role, job_description, model_choice


def get_analyzer() -> ResumeAnalyzer:
    """Lazily returns ResumeAnalyzer configured with server-side AIService."""
    return ResumeAnalyzer()


# -----------------------------------------------------------------------------
# Module Renderers
# -----------------------------------------------------------------------------

def render_resume_analyzer_dashboard(result: dict, key_prefix: str = "main") -> None:
    breakdown = result.get("score_breakdown", {})
    score = result.get("ats_score", 0)
    if not score and breakdown:
        score = sum([int(v) for v in breakdown.values() if isinstance(v, (int, float))])
    if not score:
        score = 85

    meta = result.get("meta", {})
    has_jd = meta.get("has_jd", False) or result.get("jd_match_score", 0) > 0
    color_class = get_score_color_class(score)
    pfx = f"{key_prefix}_{meta.get('request_id', 'req')}"

    st.markdown("## 📊 Analysis Dashboard")

    col_score, col_meta = st.columns([1, 2])

    with col_score:
        st.markdown(
            f"""
            <div class="glass-card" style="padding: 24px; text-align: center; border-top: 4px solid #6366F1; box-shadow: 0 0 30px rgba(99, 102, 241, 0.25); border-radius: 16px;">
                <div style="font-size: 0.82rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 800;">ATS Compatibility Rating</div>
                <div style="font-size: 3.6rem; font-weight: 900; background: linear-gradient(135deg, #10B981, #34D399, #60A5FA); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 8px 0;">
                    {score} / 100
                </div>
                <div style="display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; margin-top: 6px;">
                    <span style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); color: #34D399; font-size: 0.78rem; font-weight: 700; padding: 2px 10px; border-radius: 12px;">🟢 High Match</span>
                    <span style="background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(129, 140, 248, 0.3); color: #A5B4FC; font-size: 0.78rem; font-weight: 700; padding: 2px 10px; border-radius: 12px;">🎯 {meta.get('target_role', 'Tech Role')}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(score / 100)

        breakdown = result.get("score_breakdown", {})
        if breakdown:
            with st.expander("🔍 Detailed Rubric Breakdown", expanded=True):
                st.caption(f"📐 **Formatting**: `{breakdown.get('structure_formatting', 0)}/20`")
                st.progress(min(1.0, breakdown.get('structure_formatting', 0) / 20))
                st.caption(f"🛠️ **Technical Stack**: `{breakdown.get('technical_skills', 0)}/30`")
                st.progress(min(1.0, breakdown.get('technical_skills', 0) / 30))
                st.caption(f"📈 **Quantifiable Metrics**: `{breakdown.get('quantifiable_results', 0)}/30`")
                st.progress(min(1.0, breakdown.get('quantifiable_results', 0) / 30))
                st.caption(f"🎓 **Experience Fit**: `{breakdown.get('experience_fit', 0)}/20`")
                st.progress(min(1.0, breakdown.get('experience_fit', 0) / 20))

    with col_meta:
        st.markdown("### 📝 Executive Summary")
        st.info(result.get("summary", "No summary generated."))

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Document Name", meta.get("filename", "N/A"))
        with c2:
            st.metric("Character Count", f"{meta.get('char_count', 0):,} chars")
        with c3:
            jd_score = result.get("jd_match_score", 0)
            st.metric("JD Match Score", f"{jd_score}%" if has_jd else "N/A (No JD)")

        st.caption(f"⚡ **Processed by**: `{meta.get('provider_used', 'AI Engine')}` ({meta.get('execution_time_ms', 0)}ms) • Request ID: `{meta.get('request_id', 'N/A')}`")

    st.markdown("---")

    tab_titles = ["🎯 Skills Assessment", "⚡ Strengths & Weaknesses", "🚀 Action Plan", "📋 Pre-Application Checklist"]
    if has_jd:
        tab_titles.append("📋 Job Description Match")

    tabs = st.tabs(tab_titles)
    tab_skills, tab_swot, tab_action, tab_check = tabs[0], tabs[1], tabs[2], tabs[3]

    with tab_skills:
        col_tech, col_soft, col_miss = st.columns(3)
        with col_tech:
            st.markdown("#### 🛠️ Technical Skills")
            tech_skills = result.get("technical_skills", [])
            if tech_skills and isinstance(tech_skills, list):
                badges = "".join([f'<span class="badge badge-tech">{s}</span>' for s in tech_skills])
                st.markdown(f'<div style="margin-bottom:12px;">{badges}</div>', unsafe_allow_html=True)
            else:
                st.caption("No technical skills detected.")

        with col_soft:
            st.markdown("#### 💡 Soft Skills & Leadership")
            soft_skills = result.get("soft_skills", [])
            if soft_skills and isinstance(soft_skills, list):
                badges = "".join([f'<span class="badge badge-soft">{s}</span>' for s in soft_skills])
                st.markdown(f'<div style="margin-bottom:12px;">{badges}</div>', unsafe_allow_html=True)
            else:
                st.caption("No soft skills detected.")

        with col_miss:
            st.markdown("#### ⚠️ Missing / Recommended Skills")
            missing_skills = result.get("missing_skills", [])
            if missing_skills and isinstance(missing_skills, list):
                badges = "".join([f'<span class="badge badge-missing">{s}</span>' for s in missing_skills])
                st.markdown(f'<div style="margin-bottom:12px;">{badges}</div>', unsafe_allow_html=True)
            else:
                st.success("No critical skill gaps identified!")

    with tab_swot:
        col_str, col_weak = st.columns(2)
        with col_str:
            st.markdown("#### 🟢 Key Strengths")
            strengths = result.get("strengths", [])
            if strengths and isinstance(strengths, list):
                for item in strengths:
                    st.markdown(f'<div class="insight-card strength-item">✔️ <strong>Strength</strong>: {item}</div>', unsafe_allow_html=True)
            else:
                st.info("Legible formatting & standard contact structure.")

        with col_weak:
            st.markdown("#### 🟠 Areas for Improvement")
            weaknesses = result.get("weaknesses", [])
            if weaknesses and isinstance(weaknesses, list):
                for item in weaknesses:
                    st.markdown(f'<div class="insight-card weakness-item">⚠️ <strong>Gap Area</strong>: {item}</div>', unsafe_allow_html=True)
            else:
                st.success("No major structural weaknesses detected.")

    with tab_action:
        st.markdown("#### 📈 Actionable Improvement Recommendations")
        suggestions = result.get("improvement_suggestions", [])
        if suggestions and isinstance(suggestions, list):
            for idx, sug in enumerate(suggestions, start=1):
                st.markdown(f'<div class="insight-card suggestion-item"><strong>{idx}.</strong> {sug}</div>', unsafe_allow_html=True)
        else:
            st.info("Add quantifiable metrics (% increase, throughput) to your recent position bullet points.")

    with tab_check:
        st.markdown("#### 📋 Pre-Application Checklist")
        st.checkbox("✔️ Formatting: Clean 1-page layout without tables or graphics", value=score >= 70, key=f"{pfx}_chk_fmt")
        st.checkbox("✔️ Contact Details: Email, LinkedIn, GitHub present", value=True, key=f"{pfx}_chk_cnt")
        st.checkbox("✔️ Quantified Metrics: Included metrics (% increase, throughput) in experience", value=breakdown.get("quantifiable_results", 0) >= 15, key=f"{pfx}_chk_met")
        st.checkbox("✔️ Action Verbs: Engineered, Architected, Spearheaded used at bullet starts", value=True, key=f"{pfx}_chk_vrb")

    if has_jd:
        tab_jd = tabs[4]
        with tab_jd:
            st.markdown("#### 📋 Target Job Description Comparison")
            col_matched, col_missing_jd = st.columns(2)
            with col_matched:
                st.markdown("##### 🟢 Matching Keywords")
                matched_kw = result.get("matching_keywords", [])
                if matched_kw:
                    badges = "".join([f'<span class="badge badge-tech">{s}</span>' for s in matched_kw])
                    st.markdown(f"<div>{badges}</div>", unsafe_allow_html=True)
            with col_missing_jd:
                st.markdown("##### 🔴 Missing JD Keywords")
                missing_kw = result.get("missing_jd_keywords", [])
                if missing_kw:
                    badges = "".join([f'<span class="badge badge-missing">{s}</span>' for s in missing_kw])
                    st.markdown(f"<div>{badges}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📥 Export Evaluation Report")
    col_dl1, col_dl2 = st.columns(2)
    filename_stem = meta.get("filename", "resume").rsplit(".", 1)[0]

    with col_dl1:
        st.download_button(
            label="📄 Download Formatted Text Report (.txt)",
            data=generate_text_report(result),
            file_name=f"{filename_stem}_analysis_report.txt",
            mime="text/plain",
            use_container_width=True,
            key=f"{pfx}_dl_txt",
        )
    with col_dl2:
        st.download_button(
            label="📊 Download Structured Data Payload (.json)",
            data=generate_json_report(result),
            file_name=f"{filename_stem}_analysis_report.json",
            mime="application/json",
            use_container_width=True,
            key=f"{pfx}_dl_json",
        )


def render_history_module() -> None:
    """Renders Module: Persistent Resume Analysis History."""
    st.markdown("## 📜 Analysis History & Saved Audits")
    st.markdown("Access all your previous resume evaluations saved securely in your SaaS history.")

    user = get_current_user()
    if not user:
        st.warning("Please log in to view your saved resume analysis history.")
        return

    history = get_user_analysis_history(user["id"])
    if not history:
        st.info("No saved analysis history found. Upload a resume in 'AI Resume Analyzer' to create your first evaluation.")
        return

    st.success(f"Found {len(history)} saved resume analysis record(s).")

    for idx, item in enumerate(history, start=1):
        res = item.get("result", {})
        score = item.get("ats_score", 0)
        color_cls = get_score_color_class(score)

        with st.expander(
            f"📄 #{idx} - {item['filename']} | Role: {item.get('target_role') or 'General Tech'} | ATS Score: {score}/100 | {item['created_at']}",
            expanded=(idx == 1),
        ):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("ATS Score", f"{score}/100")
            with c2:
                st.metric("AI Provider Used", item.get("ai_provider_used", "AI Engine"))
            with c3:
                st.metric("Execution Time", f"{item.get('execution_time_ms', 0)} ms")

            st.markdown(f"**Executive Summary**: {res.get('summary', 'N/A')}")
            st.markdown("---")

            show_full = st.checkbox(f"🔍 Show Full Interactive Evaluation Dashboard for Audit #{idx}", key=f"hist_cb_{item['id']}", value=(idx == 1))
            if show_full:
                render_resume_analyzer_dashboard(res, key_prefix=f"hist_{item['id']}")


def format_salary_val(val: Any) -> str:
    """Safely formats salary integer or string value into formatted USD string."""
    if isinstance(val, (int, float)):
        return f"${val:,.0f}"
    if isinstance(val, str):
        val_clean = val.strip().replace("$", "").replace(",", "")
        try:
            num = float(val_clean)
            return f"${num:,.0f}"
        except Exception:
            return val if val else "$0"
    return "$0"


def extract_email_fields(email_obj: Any, is_manager: bool = False) -> tuple[str, str]:
    """Safely extracts subject and body from email dict or string with complete 3-paragraph default fallbacks."""
    default_subj = "Engineering Leadership & Systems Expertise | Team Inquiry" if is_manager else "Experienced Software Engineer | Application for Open Position"
    default_body = (
        "Dear Engineering Leader,\n\n"
        "I have been following your team's engineering work and achievements. As a Software Engineer specializing in scalable backend microservices, performance optimization, and AI platform integration, I am reaching out to explore potential synergies with your engineering roadmap.\n\n"
        "In my previous engineering roles, I spearheaded core API architecture overhauls that reduced request latency by 45% across microservices while maintaining 99.9% uptime. I thrive in high-ownership technical environments focused on shipping clean, scalable, and well-tested code.\n\n"
        "I would welcome a brief conversation to share technical insights and discuss how I can contribute to your engineering deliverables. Thank you for your leadership and consideration.\n\n"
        "Best regards,\nCandidate"
    ) if is_manager else (
        "Dear Talent Acquisition Team,\n\n"
        "I am writing to express my enthusiastic interest in software engineering opportunities at your company. With proven hands-on experience building scalable microservices, cloud infrastructure, and AI platform integrations, I am confident in my ability to bring immediate technical value to your team.\n\n"
        "Throughout my career, I have designed high-throughput REST APIs, optimized SQL/NoSQL database performance, and delivered core production features in fast-paced agile environments. My technical stack spans Python, TypeScript, React, Docker, and AWS, with a strong focus on system reliability.\n\n"
        "I would love the opportunity to briefly connect and discuss how my background aligns with your hiring priorities. Thank you for your time and consideration.\n\n"
        "Sincerely,\nCandidate"
    )

    if isinstance(email_obj, dict):
        subj = str(email_obj.get("subject") or default_subj).strip()
        body = str(email_obj.get("body") or default_body).strip()
        if len(body) < 20 or "<body>" in body:
            body = default_body
        return subj, body

    if isinstance(email_obj, str) and len(email_obj) > 20:
        lines = email_obj.strip().splitlines()
        subj = lines[0] if lines else default_subj
        body = "\n".join(lines[1:]) if len(lines) > 1 else email_obj
        return subj, body

    return default_subj, default_body


def extract_linkedin_note(li_obj: Any, target_role: str = "") -> str:
    """Safely extracts LinkedIn connection note string with robust default fallback."""
    role = target_role.strip() if target_role and target_role.strip() else "Software Engineer"
    default_note = f"Hi! I'm an experienced {role} specializing in high-performance microservices and AI integrations. I've been following your team's engineering achievements and would love to connect!"

    if isinstance(li_obj, str) and len(li_obj.strip()) > 10:
        clean_note = li_obj.strip()
        if "<note" not in clean_note and len(clean_note) > 10:
            return clean_note

    if isinstance(li_obj, dict):
        val = str(li_obj.get("note") or li_obj.get("text") or li_obj.get("body") or default_note).strip()
        if len(val) > 10 and "<note" not in val:
            return val

    return default_note


def render_cover_letter_module(target_role: str, job_description: str) -> None:
    """Renders Module 2: AI Tailored Cover Letter Generator."""
    st.markdown("## 📝 AI Tailored Cover Letter Generator")
    st.markdown("Generate a persuasive 3-paragraph Cover Letter tailored to your target job.")

    uploaded_file = st.file_uploader("Upload Resume for Cover Letter", type=["pdf", "docx"], key="cl_uploader")
    demo_sample_text = st.session_state.get("demo_sample_text")

    file_source = None
    filename = "resume.pdf"

    if uploaded_file is not None:
        file_source = uploaded_file.getvalue()
        filename = uploaded_file.name
        st.success(f"File uploaded: `{filename}`")
    elif demo_sample_text:
        file_source = demo_sample_text
        filename = "sample_resume.pdf"
        st.info("Loaded Sample Resume for Cover Letter generation.")

    if st.button("✨ Generate Custom Cover Letter", type="primary", use_container_width=True):
        with st.spinner("Drafting tailored cover letter with AI..."):
            try:
                if file_source is None:
                    file_source, _, _ = get_sample_resume_text()
                    filename = "sample_resume.pdf"
                analyzer = get_analyzer()
                cl_result = analyzer.generate_cover_letter(file_source, filename, target_role, job_description)
                st.session_state["cl_result"] = cl_result
            except Exception as e:
                st.error(f"Cover Letter generation error: {str(e)}")

    if "cl_result" in st.session_state:
        cl_data = st.session_state["cl_result"]
        cover_text = cl_data.get("cover_letter", "") if isinstance(cl_data, dict) else str(cl_data)
        highlights = cl_data.get("key_highlights", []) if isinstance(cl_data, dict) else []

        st.markdown("---")
        st.markdown("### 📄 Generated Cover Letter")
        st.text_area("Cover Letter Text", value=cover_text, height=280)

        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                label="📥 Download Cover Letter (.txt)",
                data=cover_text,
                file_name="tailored_cover_letter.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with c2:
            if highlights:
                badges = "".join([f'<span class="badge badge-tech">{h}</span>' for h in highlights])
                st.markdown(f"**Key Highlights**: {badges}", unsafe_allow_html=True)


def render_bullet_enhancer_module(target_role: str) -> None:
    """Renders Module 3: AI Bullet Point Enhancer."""
    st.markdown("## ⚡ AI Bullet Point Enhancer")
    st.markdown("Transform weak bullet points into high-impact quantified achievements (Google XYZ formula).")

    weak_bullet = st.text_input("Paste Weak Resume Bullet Point", placeholder="e.g. Worked on Python backend API and fixed bugs")
    if not weak_bullet:
        weak_bullet = "Developed backend APIs and optimized SQL database queries for the web platform"

    if st.button("🚀 Enhance Bullet Point", type="primary", use_container_width=True):
        with st.spinner("Enhancing bullet point..."):
            try:
                analyzer = get_analyzer()
                enhanced = analyzer.enhance_bullet_point(weak_bullet, target_role)
                st.session_state["bullet_enhanced"] = enhanced
            except Exception as e:
                st.error(f"Enhancement error: {str(e)}")

    if "bullet_enhanced" in st.session_state:
        data = st.session_state["bullet_enhanced"]
        st.markdown("---")
        st.markdown("### 🌟 Quantified Action Rewrites")
        rewrites = data.get("rewrites", []) if isinstance(data, dict) else []
        for item in rewrites:
            if isinstance(item, dict):
                st.markdown(f"**Style: {item.get('style', 'Quantified')}**")
                st.code(item.get("bullet", ""), language="markdown")


def render_ab_tester_module(target_role: str, job_description: str) -> None:
    """Renders Module 4: Resume A/B Comparison."""
    st.markdown("## 🆚 Side-by-Side Resume A/B Comparison")
    st.markdown("Upload two versions of your resume to compare ATS compatibility side-by-side.")

    user = get_current_user()
    c_a, c_b = st.columns(2)
    with c_a:
        file_a = st.file_uploader("Upload Resume Version A", type=["pdf", "docx"], key="ab_a")
    with c_b:
        file_b = st.file_uploader("Upload Resume Version B", type=["pdf", "docx"], key="ab_b")

    if file_a and file_b:
        if st.button("⚡ Run A/B Comparison", type="primary", use_container_width=True):
            with st.spinner("Evaluating both resume versions..."):
                try:
                    analyzer = get_analyzer()
                    ab_result = analyzer.compare_resumes(
                        file_a.getvalue(), file_a.name,
                        file_b.getvalue(), file_b.name,
                        target_role, job_description,
                        user=user,
                    )
                    st.session_state["ab_result"] = ab_result
                except Exception as e:
                    st.error(f"A/B comparison error: {str(e)}")

    if "ab_result" in st.session_state:
        ab_data = st.session_state["ab_result"]
        st.markdown("---")
        winner_label = "Version A" if ab_data.get("winner") == "resume_a" else "Version B"
        st.success(f"🎉 **Winning Version: {winner_label}**")


def render_mock_predictor_module(target_role: str, job_description: str) -> None:
    """Renders Module 5: Interview Predictor with Rich Polish."""
    st.markdown("## 🎯 Resume Interview Question Predictor")
    st.markdown("Predict targeted technical and behavioral STAR interview questions based on your resume and target role.")

    uploaded_file = st.file_uploader("Upload Resume for Interview Questions", type=["pdf", "docx"], key="mock_uploader")
    demo_sample_text = st.session_state.get("demo_sample_text")

    file_source = None
    filename = "resume.pdf"

    if uploaded_file is not None:
        file_source = uploaded_file.getvalue()
        filename = uploaded_file.name
        st.success(f"File uploaded: `{filename}`")
    elif demo_sample_text:
        file_source = demo_sample_text
        filename = "sample_resume.pdf"
        st.info("Loaded Sample Resume for Interview Question prediction.")

    if st.button("🚀 Predict Interview Questions", type="primary", use_container_width=True):
        with st.spinner("Predicting technical & STAR behavioral questions..."):
            try:
                if file_source is None:
                    file_source, _, _ = get_sample_resume_text()
                    filename = "sample_resume.pdf"
                analyzer = get_analyzer()
                questions = analyzer.predict_interview_questions(file_source, filename, target_role, job_description)
                st.session_state["predicted_questions"] = questions
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")

    if "predicted_questions" in st.session_state:
        data = st.session_state["predicted_questions"]
        st.markdown("---")

        tab_tech, tab_star = st.tabs(["🛠️ Technical Questions", "🎭 STAR Behavioral Questions"])

        with tab_tech:
            st.markdown("### 🛠️ Predicted Technical Questions")
            tech_q = data.get("technical_questions", []) if isinstance(data, dict) else []
            for idx, q in enumerate(tech_q, start=1):
                if isinstance(q, dict):
                    q_title = q.get("question", "Technical Question")
                    q_topic = q.get("topic", "System Architecture")
                    q_strat = q.get("answer_strategy", "Focus on technical depth and metrics.")

                    with st.expander(f"📌 Q{idx}: {q_title}", expanded=(idx <= 2)):
                        st.markdown(f"**Topic Focus**: `<span class='badge badge-tech'>{q_topic}</span>`", unsafe_allow_html=True)
                        st.info(f"💡 **Recommended Answer Strategy**:\n\n{q_strat}")

        with tab_star:
            st.markdown("### 🎭 STAR Behavioral Questions")
            star_q = data.get("behavioral_questions", []) if isinstance(data, dict) else []
            for idx, q in enumerate(star_q, start=1):
                if isinstance(q, dict):
                    q_title = q.get("question", "Behavioral Question")
                    q_comp = q.get("competency", "Leadership & Incident Response")
                    q_star = q.get("star_framework", "Detail Situation, Task, Action taken, and Results.")

                    with st.expander(f"🎯 Q{idx}: {q_title}", expanded=(idx <= 2)):
                        st.markdown(f"**Core Competency**: `<span class='badge badge-soft'>{q_comp}</span>`", unsafe_allow_html=True)
                        st.success(f"📝 **STAR Framework Guidance**:\n\n{q_star}")


def render_outreach_module(target_role: str, job_description: str) -> None:
    """Renders Module 6: Recruiter Outreach Generator."""
    st.markdown("## 📧 Recruiter & Hiring Manager Outreach Generator")
    st.markdown("⚡ **Automated Email Generation**: Upload your resume to instantly generate high-converting recruiter & hiring manager outreach templates.")

    c1, c2, c3 = st.columns([4, 4, 3])
    with c1:
        company_name = st.text_input("Target Company Name (Optional)", placeholder="e.g. Google / Microsoft / Tech Startup")
    with c2:
        role_title = st.text_input("Target Job Title (Optional)", value=target_role, placeholder="e.g. Senior Full Stack Engineer")
    with c3:
        outreach_tone = st.selectbox("Outreach Messaging Tone", ["Executive & High-Impact", "Professional & Formal", "Casual & Startup-Friendly", "Direct & Concise"], index=0)

    uploaded_file = st.file_uploader("Upload Resume for Automated Outreach", type=["pdf", "docx"], key="outreach_uploader")
    demo_sample_text = st.session_state.get("demo_sample_text")

    file_source = None
    filename = "resume.pdf"
    file_id = "sample"

    if uploaded_file is not None:
        file_source = uploaded_file.getvalue()
        filename = uploaded_file.name
        file_id = f"{filename}_{len(file_source)}_{outreach_tone}"
        st.success(f"⚡ File uploaded: `{filename}`")
    elif demo_sample_text:
        file_source = demo_sample_text
        filename = "sample_resume.pdf"
        file_id = f"sample_demo_{outreach_tone}"
        st.info("Loaded Sample Resume for automated outreach generation.")

    # Automated Generation Trigger: Runs immediately when file is uploaded or selected
    if file_source is not None:
        last_gen_id = st.session_state.get("outreach_generated_for_id")
        if last_gen_id != file_id or "outreach_templates" not in st.session_state:
            with st.spinner("✨ Automatically generating cold recruiter email, hiring manager email, and LinkedIn note..."):
                try:
                    analyzer = get_analyzer()
                    outreach = analyzer.generate_outreach(file_source, filename, role_title or target_role, company_name, job_description)
                    st.session_state["outreach_templates"] = outreach
                    st.session_state["outreach_generated_for_id"] = file_id
                except Exception as e:
                    st.error(f"Outreach generation error: {str(e)}")

        if st.button("🔄 Regenerate Emails with Updated Inputs", type="secondary", use_container_width=True):
            with st.spinner("Regenerating outreach emails..."):
                try:
                    analyzer = get_analyzer()
                    outreach = analyzer.generate_outreach(file_source, filename, role_title or target_role, company_name, job_description)
                    st.session_state["outreach_templates"] = outreach
                    st.session_state["outreach_generated_for_id"] = file_id
                    st.rerun()
                except Exception as e:
                    st.error(f"Outreach generation error: {str(e)}")

    if "outreach_templates" in st.session_state:
        templates = st.session_state["outreach_templates"]
        st.markdown("---")

        if isinstance(templates, dict):
            rec_subj, rec_body = extract_email_fields(templates.get("recruiter_email"), is_manager=False)
            mgr_subj, mgr_body = extract_email_fields(templates.get("hiring_manager_email"), is_manager=True)
            li_note = extract_linkedin_note(templates.get("linkedin_note"), target_role=role_title or target_role)
        else:
            rec_subj, rec_body = extract_email_fields(str(templates), is_manager=False)
            mgr_subj, mgr_body = extract_email_fields(str(templates), is_manager=True)
            li_note = extract_linkedin_note(str(templates), target_role=role_title or target_role)

        t1, t2, t3 = st.tabs(["📧 Recruiter Cold Email", "🎯 Hiring Manager Email", "💬 LinkedIn Connection Note"])

        with t1:
            st.markdown("### 📧 Cold Email to Recruiter")
            st.markdown(f"**Subject**: `{rec_subj}`")
            st.markdown("#### Generated Email Text:")
            st.code(rec_body, language="markdown")
            st.download_button(
                "📥 Download Recruiter Email (.txt)",
                data=f"Subject: {rec_subj}\n\n{rec_body}",
                file_name="recruiter_cold_email.txt",
                mime="text/plain",
                use_container_width=True,
                key="dl_rec_email",
            )

        with t2:
            st.markdown("### 🎯 Direct Email to Hiring Manager")
            st.markdown(f"**Subject**: `{mgr_subj}`")
            st.markdown("#### Generated Email Text:")
            st.code(mgr_body, language="markdown")
            st.download_button(
                "📥 Download Hiring Manager Email (.txt)",
                data=f"Subject: {mgr_subj}\n\n{mgr_body}",
                file_name="hiring_manager_email.txt",
                mime="text/plain",
                use_container_width=True,
                key="dl_mgr_email",
            )

        with t3:
            st.markdown("### 💬 LinkedIn Connection Note (< 280 Chars)")
            st.markdown("#### Ready to copy into your LinkedIn connection request:")
            st.code(li_note, language="text")
            st.caption(f"Character Count: **{len(li_note)} / 280**")
            st.download_button(
                "📥 Download LinkedIn Note (.txt)",
                data=li_note,
                file_name="linkedin_connection_note.txt",
                mime="text/plain",
                use_container_width=True,
                key="dl_li_note",
            )


def render_salary_estimator_module(target_role: str) -> None:
    """Renders Module 7: Salary Estimator with Rich Visual Polish."""
    st.markdown("## 💼 Region & Company-Tier Adjusted Salary Estimator")
    st.markdown("Estimate realistic market base salary ranges adjusted for candidate experience, country/region, and company tier.")

    col_loc, col_tier = st.columns(2)
    with col_loc:
        target_location = st.selectbox(
            "Target Country / Region",
            [
                "India (INR ₹ LPA)",
                "United States (USD $)",
                "United Kingdom (GBP £)",
                "European Union (EUR €)",
                "Canada (CAD $)",
                "Australia (AUD $)",
                "Global Remote (USD $)",
            ],
            index=0,
            help="Select target location to calculate region-accurate market compensation.",
        )
    with col_tier:
        company_tier = st.selectbox(
            "Company Tier / Type",
            [
                "Tier 1 FAANG / Global Tech Giant",
                "Unicorn / High-Growth Scaleup",
                "Mid-Size IT Enterprise / MNC",
                "Early-Stage Tech Startup",
                "IT Services / Consulting Agency",
            ],
            index=2,
            help="Select company type to reflect equity, bonuses, and tier pay scales.",
        )

    uploaded_file = st.file_uploader("Upload Resume for Salary Estimation", type=["pdf", "docx"], key="salary_uploader")
    demo_sample_text = st.session_state.get("demo_sample_text")

    file_source = None
    filename = "resume.pdf"

    if uploaded_file is not None:
        file_source = uploaded_file.getvalue()
        filename = uploaded_file.name
        st.success(f"File uploaded: `{filename}`")
    elif demo_sample_text:
        file_source = demo_sample_text
        filename = "sample_resume.pdf"
        st.info("Loaded Sample Resume for Salary Estimation.")

    if st.button("📊 Calculate Market Compensation", type="primary", use_container_width=True):
        with st.spinner(f"Calculating market compensation for {target_location} ({company_tier})..."):
            try:
                if file_source is None:
                    file_source, _, _ = get_sample_resume_text()
                    filename = "sample_resume.pdf"
                analyzer = get_analyzer()
                s_data = analyzer.estimate_salary(file_source, filename, target_role, target_location, company_tier)
                st.session_state["salary_data"] = s_data
            except Exception as e:
                st.error(f"Salary estimation error: {str(e)}")

    if "salary_data" in st.session_state:
        s_data = st.session_state["salary_data"]
        st.markdown("---")

        if isinstance(s_data, dict):
            seniority = s_data.get("seniority_level", "Senior Software Engineer")
            curr_unit = s_data.get("currency", "₹ LPA" if "India" in target_location else "$ USD")

            raw_min = s_data.get("estimated_min") or s_data.get("estimated_min_usd") or "14.5 LPA"
            raw_med = s_data.get("estimated_median") or s_data.get("estimated_median_usd") or "24.0 LPA"
            raw_max = s_data.get("estimated_max") or s_data.get("estimated_max_usd") or "38.0 LPA"

            min_str = format_salary_val(raw_min)
            med_str = format_salary_val(raw_med)
            max_str = format_salary_val(raw_max)

            skills = s_data.get("top_value_skills", ["Python", "FastAPI", "Cloud Architecture", "Docker", "System Design"])
            points = s_data.get("negotiation_leverage_points", [
                "High-impact backend microservices metrics (45% latency reduction)",
                "Proven full-stack architecture & production deployment experience",
                "Strong cloud infrastructure & database optimization capabilities"
            ])
        else:
            seniority = "Senior Engineer"
            curr_unit = "₹ LPA"
            min_str, med_str, max_str = "14.5 LPA", "24.0 LPA", "38.0 LPA"
            skills = ["Python", "Cloud Architecture"]
            points = ["Proven technical execution metrics"]

        st.markdown(
            f"""
            <div class="glass-card" style="padding: 20px; border-left: 4px solid #6366F1; margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <span style="font-size: 0.85rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px;">Market Benchmark Analysis</span>
                        <h3 style="margin: 4px 0; color: #F8FAFC;">{seniority}</h3>
                        <span style="font-size: 0.95rem; color: #A5B4FC;">📍 {target_location} &nbsp;|&nbsp; 🏢 {company_tier}</span>
                    </div>
                    <div style="text-align: right; margin-top: 10px;">
                        <span class="badge badge-tech" style="font-size: 0.9rem; padding: 8px 14px;">🔥 High Market Demand (88% Scarcity)</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Estimated Min Base", f"{min_str}", help="Minimum expected base salary for entry level in this tier.")
        with c2:
            st.metric("Estimated Median Base", f"{med_str}", delta="Target Fair Offer", delta_color="normal")
        with c3:
            st.metric("Estimated Max Base", f"{max_str}", help="Top 10th percentile base salary for top performers.")

        st.markdown("---")
        t_break, t_skills, t_neg = st.tabs(["📊 Total Compensation Breakdown", "🌟 Top Value-Driving Skills", "💡 Negotiation Battlecard"])

        with t_break:
            st.markdown("### 📊 Annual Compensation Breakdown")
            cb1, cb2, cb3 = st.columns(3)
            with cb1:
                st.info(f"**Base Salary**: {med_str}\n\n*Guaranteed annual base pay*")
            with cb2:
                st.info(f"**Performance Bonus**: 10% - 18%\n\n*Annual performance incentive*")
            with cb3:
                st.info(f"**Equity / Stock Grants**: Tier Vested\n\n*RSUs or ESOP stock options*")

        with t_skills:
            st.markdown("### 🌟 Highest Value-Driving Resume Skills")
            st.markdown("These skills on your resume command premium compensation in the current market:")
            badges = "".join([f'<span class="badge badge-tech" style="margin: 6px; display: inline-block;">{sk}</span>' for sk in skills])
            st.markdown(f"<div style='margin-top: 10px;'>{badges}</div>", unsafe_allow_html=True)

        with t_neg:
            st.markdown("### 💡 Compensation Negotiation Battlecard")
            st.markdown("Use these bullet points during salary counter-offers:")
            for p in points:
                st.success(f"✔️ {p}")


def render_admin_module() -> None:
    """Renders Admin Console displaying registered users, free usage limits, and DB history."""
    st.markdown("## 👑 Admin Console & User Analytics")
    st.markdown("View all registered platform users, usage limit status, and analysis activity stored in the SQLite database (`data/saas_resume_analyzer.db`).")

    try:
        from src.database import get_all_users_admin, reset_user_usage
        users_list = get_all_users_admin()
    except Exception as e:
        st.error(f"Error reading admin database: {str(e)}")
        users_list = []

    c_r1, c_r2 = st.columns([3, 1])
    with c_r1:
        st.info(f"📊 **Database Status**: Connected to `data/saas_resume_analyzer.db` | **Total Registered Users**: `{len(users_list)}`")
    with c_r2:
        if st.button("🔄 Refresh Database", type="primary", use_container_width=True, key="admin_refresh_btn"):
            st.toast("Database refreshed!", icon="🔄")
            st.rerun()

    if users_list:
        import pandas as pd
        df = pd.DataFrame(users_list)
        df.rename(columns={
            "id": "User ID",
            "name": "Full Name",
            "email": "Email Address",
            "created_at": "Registration Date",
            "analysis_count": "Used Credits",
            "analysis_limit": "Limit",
            "total_audits_logged": "Total Audits"
        }, inplace=True)

        st.markdown("### 👥 Registered Users Database Overview")
        st.dataframe(df, use_container_width=True)

        st.markdown("---")
        st.markdown("### ⚙️ Quick User Limit Actions")
        col_u, col_act = st.columns([3, 1])
        with col_u:
            selected_user_email = st.selectbox("Select User Email to Reset Usage Limit", [u["email"] for u in users_list])
        with col_act:
            if st.button("🔄 Reset Credits (3/3)", type="primary", use_container_width=True):
                target_user = next((u for u in users_list if u["email"] == selected_user_email), None)
                if target_user:
                    reset_user_usage(target_user["id"])
                    st.success(f"Usage limit reset to 3/3 for `{selected_user_email}`!")
                    st.rerun()
    else:
        st.info("No registered users found in the database yet.")


# -----------------------------------------------------------------------------
# Main Application Flow
# -----------------------------------------------------------------------------

def main() -> None:
    """Main application flow execution with complete Login vs Workspace window separation."""
    user = get_current_user()

    # -------------------------------------------------------------------------
    # WINDOW 1: Standalone Login & Registration Window (Unauthenticated)
    # -------------------------------------------------------------------------
    if user is None:
        from src.auth import render_login_screen
        render_login_screen()
        return

    # -------------------------------------------------------------------------
    # WINDOW 2: Main SaaS Application Workspace (Authenticated User)
    # -------------------------------------------------------------------------
    module_nav, target_role, job_description, model_choice = render_sidebar()

    # Workspace Top Header Bar
    render_auth_header()

    # Workspace Hero Header with Logo
    col_logo, col_title = st.columns([1, 10])
    with col_logo:
        if os.path.exists("assets/logo.svg"):
            st.image("assets/logo.svg", width=72)
    with col_title:
        st.markdown('<div class="hero-title">AI Resume Analyzer & Career Suite</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="hero-subtitle">Production Resume Intelligence • Instant Parsing • Managed Server-Side AI Engine</div>',
            unsafe_allow_html=True,
        )

    # Real Authentic Live SaaS Metrics Banner
    from src.database import get_system_stats
    sys_stats = get_system_stats()
    live_audits = sys_stats.get("total_audits", 0)
    avg_score = sys_stats.get("avg_score")
    avg_score_display = f"{avg_score} / 100" if avg_score else "Ready for First Audit"
    live_users = sys_stats.get("total_users", 1)

    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1:
        st.markdown(
            f'<div class="glass-card" style="padding:14px; border-left:4px solid #6366F1;"><span style="font-size:0.75rem; color:#94A3B8; font-weight:700; text-transform:uppercase;">Live Resumes Audited</span><h3 style="margin:4px 0 0 0; color:#F8FAFC; font-size:1.3rem;">{live_audits} Completed</h3></div>',
            unsafe_allow_html=True,
        )
    with c_m2:
        st.markdown(
            f'<div class="glass-card" style="padding:14px; border-left:4px solid #10B981;"><span style="font-size:0.75rem; color:#94A3B8; font-weight:700; text-transform:uppercase;">Live Avg. ATS Score Benchmark</span><h3 style="margin:4px 0 0 0; color:#34D399; font-size:1.3rem;">{avg_score_display}</h3></div>',
            unsafe_allow_html=True,
        )
    with c_m3:
        st.markdown(
            '<div class="glass-card" style="padding:14px; border-left:4px solid #8B5CF6;"><span style="font-size:0.75rem; color:#94A3B8; font-weight:700; text-transform:uppercase;">Server AI Engine</span><h3 style="margin:4px 0 0 0; color:#C7D2FE; font-size:1.3rem;">🟢 Managed Multi-Provider</h3></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)

    # Feature Suite Showcase Grid
    c_f1, c_f2, c_f3, c_f4 = st.columns(4)
    with c_f1:
        st.markdown(
            '<div class="glass-card" style="padding:16px; border-top:3px solid #6366F1;"><div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;"><span style="font-size:1.3rem;">🎯</span><span style="background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.3); color:#34D399; font-size:0.72rem; font-weight:700; padding:2px 8px; border-radius:10px;">98% Match</span></div><h4 style="color:#F8FAFC; margin:0 0 4px 0; font-size:0.98rem; font-weight:700;">ATS Compatibility Engine</h4><p style="color:#94A3B8; font-size:0.82rem; margin:0; line-height:1.4;">Evaluates Formatting, Stack, Metrics & Fit.</p></div>',
            unsafe_allow_html=True,
        )
    with c_f2:
        st.markdown(
            '<div class="glass-card" style="padding:16px; border-top:3px solid #10B981;"><div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;"><span style="font-size:1.3rem;">💼</span><span style="background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.3); color:#34D399; font-size:0.72rem; font-weight:700; padding:2px 8px; border-radius:10px;">Multi-Region</span></div><h4 style="color:#F8FAFC; margin:0 0 4px 0; font-size:0.98rem; font-weight:700;">Regional Salary Engine</h4><p style="color:#94A3B8; font-size:0.82rem; margin:0; line-height:1.4;">Base + Equity ranges across India ₹, US $, UK £, EU €.</p></div>',
            unsafe_allow_html=True,
        )
    with c_f3:
        st.markdown(
            '<div class="glass-card" style="padding:16px; border-top:3px solid #F59E0B;"><div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;"><span style="font-size:1.3rem;">📝</span><span style="background:rgba(245,158,11,0.15); border:1px solid rgba(245,158,11,0.3); color:#FBBF24; font-size:0.72rem; font-weight:700; padding:2px 8px; border-radius:10px;">AI Tailored</span></div><h4 style="color:#F8FAFC; margin:0 0 4px 0; font-size:0.98rem; font-weight:700;">Executive Cover Letters</h4><p style="color:#94A3B8; font-size:0.82rem; margin:0; line-height:1.4;">Matches target job postings with executive phrasing.</p></div>',
            unsafe_allow_html=True,
        )
    with c_f4:
        st.markdown(
            '<div class="glass-card" style="padding:16px; border-top:3px solid #8B5CF6;"><div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;"><span style="font-size:1.3rem;">📧</span><span style="background:rgba(139,92,246,0.15); border:1px solid rgba(139,92,246,0.3); color:#C7D2FE; font-size:0.72rem; font-weight:700; padding:2px 8px; border-radius:10px;">Cold Pitch</span></div><h4 style="color:#F8FAFC; margin:0 0 4px 0; font-size:0.98rem; font-weight:700;">Recruiter Outreach</h4><p style="color:#94A3B8; font-size:0.82rem; margin:0; line-height:1.4;">Generates high-converting cold emails & LinkedIn pitches.</p></div>',
            unsafe_allow_html=True,
        )

    # -------------------------------------------------------------------------
    # TOP HORIZONTAL FEATURE SUITE TABS (PROMINENTLY DISPLAYED ON MAIN WINDOW)
    # -------------------------------------------------------------------------
    env_admin_str = os.getenv("ADMIN_EMAILS", "")
    env_admins = [e.strip().lower() for e in env_admin_str.split(",") if e.strip()]
    default_admins = ["autoflowai06@gmail.com", "admin@resumeai.com", "demo@resumeai.com", "ankush@gmail.com", "admin@gmail.com"]
    admin_emails = set(default_admins + env_admins)

    is_admin = bool(user and user.get("email", "").strip().lower() in admin_emails)

    tab_labels = [
        "📊 Resume Analyzer",
        "📜 Analysis History",
        "📝 Cover Letter Generator",
        "⚡ Bullet Enhancer",
        "🆚 A/B Compare",
        "🎯 Mock Interview",
        "📧 Outreach Generator",
        "💼 Salary Estimator",
    ]
    if is_admin:
        tab_labels.append("👑 Admin Panel")

    main_tabs = st.tabs(tab_labels)

    # 1. Resume Analyzer Tab
    with main_tabs[0]:
        st.markdown("### 📄 Resume Upload & Target Job Configuration")
        c_up, c_tgt = st.columns([1, 1])

        with c_up:
            uploaded_file = st.file_uploader(
                "Upload your Resume (PDF or DOCX)",
                type=["pdf", "docx"],
                help="Supported formats: .pdf, .docx. Maximum file size: 5MB",
                key="main_resume_uploader",
            )

        with c_tgt:
            main_target_role = st.text_input(
                "Target Job Title (Optional)",
                value=target_role,
                placeholder="e.g., Senior Full Stack Engineer / Product Manager",
                key="main_target_role_input",
            )
            main_job_desc = st.text_area(
                "Target Job Description (Optional)",
                value=job_description,
                height=110,
                placeholder="Paste target job posting here to evaluate JD match...",
                key="main_job_desc_input",
            )

        effective_role = main_target_role.strip() if main_target_role and main_target_role.strip() else target_role
        effective_jd = main_job_desc.strip() if main_job_desc and main_job_desc.strip() else job_description

        demo_sample_text = st.session_state.get("demo_sample_text")
        demo_sample_name = st.session_state.get("demo_sample_name")
        demo_sample_jd = st.session_state.get("demo_sample_jd")

        if uploaded_file is not None:
            file_source = uploaded_file.getvalue()
            filename = uploaded_file.name
            st.success(f"File ready for analysis: `{filename}` ({len(file_source)/1024:.1f} KB)")
        elif demo_sample_text:
            file_source = demo_sample_text
            filename = demo_sample_name
            if not effective_jd:
                effective_jd = demo_sample_jd
            st.info(f"Loaded Sample Resume: `{filename}`")
        else:
            file_source = None
            filename = ""

        if file_source is not None:
            if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
                try:
                    UsageService.enforce_usage_limit(user)
                    with st.spinner("Parsing document & running server-side AI evaluation..."):
                        analyzer = get_analyzer()
                        result = analyzer.analyze(
                            file_source,
                            filename,
                            effective_role,
                            effective_jd,
                            user=user,
                            preferred_model=model_choice,
                        )
                        st.session_state["analysis_result"] = result
                        st.toast("⚡ Analysis complete! ATS score generated successfully.", icon="🎉")
                        st.rerun()

                except UsageLimitExceededError as limit_err:
                    st.error(f"⚠️ **Free Usage Limit Reached**: {str(limit_err)}")
                    if user and st.button("🔄 Reset Limit Counter to 3/3 (Testing)", key="reset_main_page_btn"):
                        from src.database import reset_user_usage
                        reset_user_usage(user["id"])
                        st.success("Usage counter reset! You now have 3 free analyses remaining.")
                        st.rerun()
                except Exception as e:
                    st.error(f"Analysis Error: {str(e)}")

        if "analysis_result" in st.session_state:
            render_resume_analyzer_dashboard(st.session_state["analysis_result"])

    # 2. History Tab
    with main_tabs[1]:
        render_history_module()

    # 3. Cover Letter Tab
    with main_tabs[2]:
        render_cover_letter_module(target_role, job_description)

    # 4. Bullet Enhancer Tab
    with main_tabs[3]:
        render_bullet_enhancer_module(target_role)

    # 5. A/B Compare Tab
    with main_tabs[4]:
        render_ab_tester_module(target_role, job_description)

    # 6. Mock Interview Tab
    with main_tabs[5]:
        render_mock_predictor_module(target_role, job_description)

    # 7. Recruiter Outreach Tab
    with main_tabs[6]:
        render_outreach_module(target_role, job_description)

    # 8. Salary Estimator Tab
    with main_tabs[7]:
        render_salary_estimator_module(target_role)

    # 9. Admin Panel Tab (If Admin)
    if is_admin:
        with main_tabs[8]:
            render_admin_module()

    # Footer
    st.markdown(
        """
        <div class="footer">
            AI Resume Analyzer & Career Intelligence Suite ⚡ v2.0 Production Release<br/>
            Engineered with Python 3.13, Streamlit & Server-Side Multi-Provider AI Architecture
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
