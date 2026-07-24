"""
Streamlit Web Application Entrypoint
AI Resume Analyzer & Complete Resume Engineering Suite
"""

import os
import streamlit as st
from src.config import config
from src.logger import logger
from src.analyzer import ResumeAnalyzer, AnalysisError
from src.parser import UnsupportedFileTypeError, ParsingError
from src.llm import LLMAuthenticationError, LLMQuotaExhaustedError
from src.utils import generate_text_report, generate_json_report, get_sample_resume_text

# -----------------------------------------------------------------------------
# Page Configuration & Glassmorphism Theme Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer ⚡",
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
      const particleCount = 500;
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

# Custom Styling (CSS Injection - Full Streamlit Glassmorphic Overrides)
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

    .main .block-container {
        position: relative !important;
        z-index: 1 !important;
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 1260px !important;
    }

    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.75) !important;
        backdrop-filter: blur(16px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    .hero-title {
        font-size: 3rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        background: linear-gradient(135deg, #818CF8 0%, #C084FC 45%, #F472B6 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 0.3rem !important;
    }

    .hero-subtitle {
        color: #94A3B8 !important;
        font-size: 1.15rem !important;
        font-weight: 500 !important;
        margin-bottom: 1.4rem !important;
    }

    .trust-badge {
        display: inline-flex !important;
        align-items: center !important;
        gap: 8px !important;
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        color: #34D399 !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        padding: 6px 18px !important;
        border-radius: 30px !important;
        margin-bottom: 1.8rem !important;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.2) !important;
    }

    .score-container {
        text-align: center !important;
        padding: 36px 24px !important;
        border-radius: 24px !important;
        background: radial-gradient(135% 100% at 50% 0%, rgba(99, 102, 241, 0.22) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border: 1px solid rgba(99, 102, 241, 0.4) !important;
        box-shadow: 0 20px 50px -15px rgba(0, 0, 0, 0.7), inset 0 1px 0 0 rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(16px) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
    }
    .score-container:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 30px 70px -12px rgba(99, 102, 241, 0.35) !important;
    }

    .score-number {
        font-size: 5rem !important;
        font-weight: 800 !important;
        line-height: 1 !important;
        letter-spacing: -0.03em !important;
        margin: 14px 0 !important;
    }
    .score-high { color: #34D399 !important; text-shadow: 0 0 30px rgba(52, 211, 153, 0.5) !important; }
    .score-med { color: #FBBF24 !important; text-shadow: 0 0 30px rgba(251, 191, 36, 0.5) !important; }
    .score-low { color: #F87171 !important; text-shadow: 0 0 30px rgba(248, 113, 113, 0.5) !important; }

    .score-label {
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        color: #94A3B8 !important;
    }

    .badge {
        display: inline-block !important;
        padding: 8px 18px !important;
        margin: 6px !important;
        border-radius: 20px !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    .badge:hover { transform: scale(1.06) !important; }
    .badge-tech { background: rgba(99, 102, 241, 0.2) !important; color: #A5B4FC !important; border: 1px solid rgba(99, 102, 241, 0.5) !important; }
    .badge-soft { background: rgba(168, 85, 247, 0.2) !important; color: #E9D5FF !important; border: 1px solid rgba(168, 85, 247, 0.5) !important; }
    .badge-missing { background: rgba(239, 68, 68, 0.2) !important; color: #FCA5A5 !important; border: 1px solid rgba(239, 68, 68, 0.5) !important; }

    .insight-card {
        padding: 20px 22px !important;
        border-radius: 16px !important;
        margin-bottom: 16px !important;
        font-size: 0.98rem !important;
        line-height: 1.65 !important;
        backdrop-filter: blur(10px) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    .insight-card:hover {
        transform: translateX(6px) !important;
    }
    .strength-item {
        background: rgba(16, 185, 129, 0.08) !important;
        border-left: 4px solid #10B981 !important;
        border-top: 1px solid rgba(16, 185, 129, 0.2) !important;
        border-right: 1px solid rgba(16, 185, 129, 0.2) !important;
        border-bottom: 1px solid rgba(16, 185, 129, 0.2) !important;
        color: #F8FAFC !important;
    }
    .weakness-item {
        background: rgba(245, 158, 11, 0.08) !important;
        border-left: 4px solid #F59E0B !important;
        border-top: 1px solid rgba(245, 158, 11, 0.2) !important;
        border-right: 1px solid rgba(245, 158, 11, 0.2) !important;
        border-bottom: 1px solid rgba(245, 158, 11, 0.2) !important;
        color: #F8FAFC !important;
    }
    .suggestion-item {
        background: rgba(99, 102, 241, 0.08) !important;
        border-left: 4px solid #6366F1 !important;
        border-top: 1px solid rgba(99, 102, 241, 0.2) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.2) !important;
        border-bottom: 1px solid rgba(99, 102, 241, 0.2) !important;
        color: #F8FAFC !important;
    }

    .stButton > button {
        border-radius: 14px !important;
        font-weight: 700 !important;
        padding: 12px 24px !important;
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
        border: none !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35) !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5) !important;
    }

    button[data-baseweb="tab"] {
        font-weight: 700 !important;
        font-size: 0.98rem !important;
        padding: 12px 24px !important;
        border-radius: 12px !important;
        color: #94A3B8 !important;
    }
    button[aria-selected="true"] {
        color: #818CF8 !important;
        background: rgba(99, 102, 241, 0.12) !important;
        border-bottom: 2px solid #818CF8 !important;
    }

    [data-testid="stFileUploader"] {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 2px dashed rgba(99, 102, 241, 0.4) !important;
        border-radius: 18px !important;
        padding: 24px !important;
        backdrop-filter: blur(10px) !important;
    }

    .footer {
        text-align: center !important;
        padding: 36px 20px !important;
        color: #64748B !important;
        font-size: 0.9rem !important;
        border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
        margin-top: 60px !important;
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
    """Renders application sidebar for Resume Engineering modules and system status."""
    with st.sidebar:
        if os.path.exists("assets/logo.svg"):
            st.image("assets/logo.svg", width=64)

        st.markdown("### 🧭 Resume Suite Modules")
        module_nav = st.radio(
            "Select Resume Tool",
            [
                "📊 AI Resume Analyzer",
                "📝 Cover Letter Generator",
                "⚡ Bullet Point Enhancer",
                "🆚 Resume A/B Comparison",
                "🎯 Resume Interview Predictor",
                "📧 Recruiter Outreach Generator",
                "💼 Salary & Readiness Estimator",
            ],
            index=0,
        )

        st.markdown("---")
        st.markdown("### ⚙️ Settings & Options")

        model_choice = st.selectbox(
            "AI Model Engine",
            ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash-latest"],
            index=0,
            help="Select the Gemini model tier.",
        )

        target_role = st.text_input(
            "Target Job Title (Optional)",
            placeholder="e.g., Senior Full Stack Developer",
            help="Providing a target role improves keyword alignment.",
        )

        job_description = st.text_area(
            "Target Job Description (Optional)",
            height=120,
            placeholder="Paste target job description text here...",
            help="Paste full job description for targeted JD matching.",
        )

        st.markdown("---")
        st.markdown("### 🧪 Quick 1-Click Demo")
        if st.button("Load Sample Senior Developer Resume", use_container_width=True):
            sample_text, sample_name, sample_jd = get_sample_resume_text()
            st.session_state["demo_sample_text"] = sample_text
            st.session_state["demo_sample_name"] = sample_name
            st.session_state["demo_sample_jd"] = sample_jd
            st.success("Sample resume & JD loaded! Click 'Analyze Resume' below.")

        st.markdown("---")
        st.markdown("### 🔑 System Status")

        if config.GEMINI_API_KEY:
            st.success("Gemini API Key: Configured (.env)")
        else:
            st.warning("Gemini API Key: Not Found")
            user_key = st.text_input(
                "Enter Gemini API Key",
                type="password",
                help="Get your key from Google AI Studio",
            )
            if user_key:
                st.session_state["custom_api_key"] = user_key
                st.info("Using temporary session API key")

        with st.expander("💡 How to get a free API Key (30s)", expanded=False):
            st.markdown(
                """
                1. Visit **[Google AI Studio](https://aistudio.google.com/)**
                2. Click **Create API Key**
                3. Copy your key and paste it above!
                """
            )

        st.markdown("---")
        st.markdown(
            """
            🔒 **Enterprise Data Security**
            - **Processing**: 100% In-Memory
            - **Privacy**: Zero File Retention
            """
        )
        return module_nav, target_role, job_description, model_choice


def get_analyzer(model_choice: str) -> ResumeAnalyzer:
    """Helper function to lazily initialize ResumeAnalyzer with API key validation."""
    custom_key = st.session_state.get("custom_api_key") or config.GEMINI_API_KEY
    if not custom_key:
        st.error("🔑 **Gemini API Key Missing**: Please enter your Gemini API key in the sidebar under 'System Status' or add `GEMINI_API_KEY=your_key` to a `.env` file.")
        st.stop()
    from src.llm import GeminiClient
    llm_client = GeminiClient(api_key=custom_key, model_name=model_choice)
    return ResumeAnalyzer(llm_client=llm_client)


# -----------------------------------------------------------------------------
# Module Renderers
# -----------------------------------------------------------------------------

def render_resume_analyzer_dashboard(result: dict) -> None:
    """Renders structured analysis results in visual cards and tabs."""
    score = result.get("ats_score", 0)
    meta = result.get("meta", {})
    has_jd = meta.get("has_jd", False) or result.get("jd_match_score", 0) > 0
    color_class = get_score_color_class(score)

    st.markdown("## 📊 Analysis Dashboard")

    col_score, col_meta = st.columns([1, 2])

    with col_score:
        st.markdown(
            f"""
            <div class="score-container">
                <div class="score-label">ATS Compatibility Score</div>
                <div class="score-number {color_class}">{score}/100</div>
                <span style="color: #9CA3AF; font-size: 0.9rem;">Target: {meta.get('target_role', 'General Tech')}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(score / 100)

        breakdown = result.get("score_breakdown", {})
        if breakdown:
            with st.expander("🔍 View Score Category Breakdown", expanded=False):
                st.caption(f"📐 **Formatting**: {breakdown.get('structure_formatting', 0)}/20")
                st.caption(f"🛠️ **Technical Skills**: {breakdown.get('technical_skills', 0)}/30")
                st.caption(f"📈 **Quantifiable Impact**: {breakdown.get('quantifiable_results', 0)}/30")
                st.caption(f"🎓 **Experience Fit**: {breakdown.get('experience_fit', 0)}/20")

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

        if meta.get("cached"):
            st.caption("⚡ **Loaded from Cache** — 0 API tokens consumed.")

    st.markdown("---")

    tab_titles = ["🎯 Skills Assessment", "⚡ Strengths & Weaknesses", "🚀 Action Plan & Suggestions", "📋 Pre-Application Checklist"]
    if has_jd:
        tab_titles.append("📋 Job Description Match")

    tabs = st.tabs(tab_titles)
    tab_skills, tab_swot, tab_action, tab_check = tabs[0], tabs[1], tabs[2], tabs[3]

    with tab_skills:
        col_tech, col_soft, col_miss = st.columns(3)

        with col_tech:
            st.markdown("#### 🛠️ Technical Skills")
            tech_skills = result.get("technical_skills", [])
            if tech_skills:
                badges = "".join([f'<span class="badge badge-tech">{s}</span>' for s in tech_skills])
                st.markdown(f"<div>{badges}</div>", unsafe_allow_html=True)
            else:
                st.caption("No technical skills detected.")

        with col_soft:
            st.markdown("#### 💡 Soft Skills & Leadership")
            soft_skills = result.get("soft_skills", [])
            if soft_skills:
                badges = "".join([f'<span class="badge badge-soft">{s}</span>' for s in soft_skills])
                st.markdown(f"<div>{badges}</div>", unsafe_allow_html=True)
            else:
                st.caption("No soft skills detected.")

        with col_miss:
            st.markdown("#### ⚠️ Missing / Recommended Skills")
            missing_skills = result.get("missing_skills", [])
            if missing_skills:
                badges = "".join([f'<span class="badge badge-missing">{s}</span>' for s in missing_skills])
                st.markdown(f"<div>{badges}</div>", unsafe_allow_html=True)
            else:
                st.success("No critical skill gaps identified!")

    with tab_swot:
        col_str, col_weak = st.columns(2)

        with col_str:
            st.markdown("#### 🟢 Key Strengths")
            strengths = result.get("strengths", [])
            for item in strengths:
                st.markdown(
                    f'<div class="insight-card strength-item">✔️ {item}</div>',
                    unsafe_allow_html=True,
                )

        with col_weak:
            st.markdown("#### 🟠 Areas for Improvement")
            weaknesses = result.get("weaknesses", [])
            for item in weaknesses:
                st.markdown(
                    f'<div class="insight-card weakness-item">⚠️ {item}</div>',
                    unsafe_allow_html=True,
                )

    with tab_action:
        st.markdown("#### 📈 Actionable Improvement Suggestions")
        suggestions = result.get("improvement_suggestions", [])
        for idx, sug in enumerate(suggestions, start=1):
            st.markdown(
                f'<div class="insight-card suggestion-item"><strong>{idx}.</strong> {sug}</div>',
                unsafe_allow_html=True,
            )

    with tab_check:
        st.markdown("#### 📋 Pre-Application Pre-Flight Checklist")
        st.checkbox("✔️ Formatting: Clean 1-page layout without tables or graphics", value=score >= 70)
        st.checkbox("✔️ Contact Details: Email, LinkedIn, GitHub, Phone number present", value=True)
        st.checkbox("✔️ Quantified Metrics: Metrics (% increase, throughput, cost savings) included in bullets", value=breakdown.get("quantifiable_results", 0) >= 15)
        st.checkbox("✔️ Strong Action Verbs: Engineered, Architected, Spearheaded used at bullet starts", value=True)
        st.checkbox("✔️ Target Role Alignment: Technical skills match target industry expectations", value=score >= 80)

    if has_jd:
        tab_jd = tabs[4]
        with tab_jd:
            st.markdown("#### 📋 Target Job Description Comparison")

            col_matched, col_missing_jd = st.columns(2)

            with col_matched:
                st.markdown("##### 🟢 Matching Keywords & Skills")
                matched_kw = result.get("matching_keywords", [])
                if matched_kw:
                    badges = "".join([f'<span class="badge badge-tech">{s}</span>' for s in matched_kw])
                    st.markdown(f"<div>{badges}</div>", unsafe_allow_html=True)
                else:
                    st.caption("No exact keyword matches found.")

            with col_missing_jd:
                st.markdown("##### 🔴 Missing JD Keywords")
                missing_kw = result.get("missing_jd_keywords", [])
                if missing_kw:
                    badges = "".join([f'<span class="badge badge-missing">{s}</span>' for s in missing_kw])
                    st.markdown(f"<div>{badges}</div>", unsafe_allow_html=True)
                else:
                    st.success("Great job! No major JD keywords are missing.")

            st.markdown("---")
            st.markdown("##### 🎯 JD Alignment Recommendations")
            jd_sug = result.get("jd_tailored_suggestions", [])
            for idx, sug in enumerate(jd_sug, start=1):
                st.markdown(
                    f'<div class="insight-card suggestion-item"><strong>{idx}.</strong> {sug}</div>',
                    unsafe_allow_html=True,
                )

    # Export & Download Section
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
        )

    with col_dl2:
        st.download_button(
            label="📊 Download Structured Data Payload (.json)",
            data=generate_json_report(result),
            file_name=f"{filename_stem}_analysis_report.json",
            mime="application/json",
            use_container_width=True,
        )


def render_cover_letter_module(model_choice: str, target_role: str, job_description: str) -> None:
    """Renders Module 2: AI Tailored Cover Letter Generator."""
    st.markdown("## 📝 AI Tailored Cover Letter Generator")
    st.markdown("Generate a persuasive, customized 3-paragraph Cover Letter tailored to your target job.")

    uploaded_file = st.file_uploader(
        "Upload Resume for Cover Letter",
        type=["pdf", "docx"],
        key="cl_uploader",
    )

    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        filename = uploaded_file.name

        if st.button("✨ Generate Custom Cover Letter", type="primary", use_container_width=True):
            with st.spinner("Drafting tailored cover letter with Gemini AI..."):
                try:
                    analyzer = get_analyzer(model_choice)
                    cl_result = analyzer.generate_cover_letter(file_bytes, filename, target_role, job_description)
                    st.session_state["cl_result"] = cl_result
                except Exception as e:
                    st.error(f"Cover Letter generation error: {str(e)}")

    if "cl_result" in st.session_state:
        cl_data = st.session_state["cl_result"]
        cover_text = cl_data.get("cover_letter", "")

        st.markdown("---")
        st.markdown("### 📄 Generated Cover Letter")
        st.text_area("Cover Letter Text", value=cover_text, height=320)

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.download_button(
                label="📥 Download Cover Letter (.txt)",
                data=cover_text,
                file_name="tailored_cover_letter.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with col_c2:
            st.info("💡 Highlighted Skills: " + ", ".join(cl_data.get("key_highlights", [])))


def render_bullet_enhancer_module(model_choice: str, target_role: str) -> None:
    """Renders Module 3: AI Bullet Point Enhancer & Action Verb Rewriter."""
    st.markdown("## ⚡ AI Bullet Point Enhancer & Metric Rewriter")
    st.markdown("Transform weak, passive bullet points into high-impact, quantified achievements using the Google XYZ formula.")

    weak_bullet = st.text_input(
        "Paste Weak Resume Bullet Point",
        placeholder="e.g. Worked on Python backend API and fixed bugs for the team",
    )

    if st.button("🚀 Enhance Bullet Point", type="primary", use_container_width=True):
        if not weak_bullet.strip():
            st.warning("Please paste a bullet point to enhance.")
        else:
            with st.spinner("Rewriting with action verbs and quantifiable metrics..."):
                try:
                    analyzer = get_analyzer(model_choice)
                    enhanced = analyzer.enhance_bullet_point(weak_bullet, target_role)
                    st.session_state["bullet_enhanced"] = enhanced
                except Exception as e:
                    st.error(f"Enhancement error: {str(e)}")

    if "bullet_enhanced" in st.session_state:
        data = st.session_state["bullet_enhanced"]
        st.markdown("---")
        st.markdown("### 🌟 High-Impact Bullet Point Rewrites")

        for item in data.get("rewrites", []):
            st.markdown(f"**Style: {item.get('style', 'Quantified')}**")
            st.code(item.get("bullet", ""), language="markdown")


def render_ab_tester_module(model_choice: str, target_role: str, job_description: str) -> None:
    """Renders Module 4: Side-by-Side Resume A/B Comparison."""
    st.markdown("## 🆚 Side-by-Side Resume A/B Comparison")
    st.markdown("Upload two versions of your resume to compare ATS compatibility scores and skill counts side-by-side.")

    c_a, c_b = st.columns(2)
    with c_a:
        file_a = st.file_uploader("Upload Resume Version A", type=["pdf", "docx"], key="ab_a")
    with c_b:
        file_b = st.file_uploader("Upload Resume Version B", type=["pdf", "docx"], key="ab_b")

    if file_a and file_b:
        if st.button("⚡ Run Side-by-Side A/B Comparison", type="primary", use_container_width=True):
            with st.spinner("Evaluating both resume versions..."):
                try:
                    analyzer = get_analyzer(model_choice)
                    ab_result = analyzer.compare_resumes(
                        file_a.getvalue(), file_a.name,
                        file_b.getvalue(), file_b.name,
                        target_role, job_description,
                    )
                    st.session_state["ab_result"] = ab_result
                except Exception as e:
                    st.error(f"A/B comparison error: {str(e)}")

    if "ab_result" in st.session_state:
        ab_data = st.session_state["ab_result"]
        res_a, res_b = ab_data["resume_a"], ab_data["resume_b"]

        st.markdown("---")
        st.markdown("### 🏆 Comparison Results")

        winner_label = "Version A" if ab_data["winner"] == "resume_a" else "Version B"
        st.success(f"🎉 **Winning Version: {winner_label}**")

        col_m_a, col_m_b = st.columns(2)
        with col_m_a:
            st.markdown("### 📄 Resume Version A")
            st.metric("ATS Score", f"{res_a.get('ats_score', 0)}/100")
            st.metric("Technical Skills Count", len(res_a.get("technical_skills", [])))
            st.info(res_a.get("summary", "N/A"))

        with col_m_b:
            st.markdown("### 📄 Resume Version B")
            st.metric("ATS Score", f"{res_b.get('ats_score', 0)}/100")
            st.metric("Technical Skills Count", len(res_b.get("technical_skills", [])))
            st.info(res_b.get("summary", "N/A"))


def render_mock_predictor_module(model_choice: str, target_role: str, job_description: str) -> None:
    """Renders Module 5: AI Resume Mock Interview Predictor."""
    st.markdown("## 🎯 Resume AI Mock Interview Predictor")
    st.markdown("Predict 10 targeted Technical & STAR Behavioral questions based on your resume and target JD.")

    uploaded_file = st.file_uploader("Upload Resume for Question Prediction", type=["pdf", "docx"], key="mock_uploader")

    if uploaded_file is not None:
        if st.button("🚀 Predict My Interview Questions", type="primary", use_container_width=True):
            with st.spinner("Analyzing resume against recruiter expectations..."):
                try:
                    analyzer = get_analyzer(model_choice)
                    q_result = analyzer.predict_interview_questions(uploaded_file.getvalue(), uploaded_file.name, target_role, job_description)
                    st.session_state["mock_questions"] = q_result
                except Exception as e:
                    st.error(f"Prediction error: {str(e)}")

    if "mock_questions" in st.session_state:
        q_data = st.session_state["mock_questions"]
        st.markdown("---")
        st.markdown("#### 💻 Predicted Technical Questions")
        for idx, q in enumerate(q_data.get("technical_questions", []), 1):
            with st.expander(f"Tech Q{idx}: {q.get('question', '')}", expanded=False):
                st.caption(f"Topic: {q.get('topic', 'Core Tech')}")
                st.success(f"Strategy: {q.get('answer_strategy', '')}")

        st.markdown("#### 🗣️ Predicted Behavioral Questions (STAR Method)")
        for idx, q in enumerate(q_data.get("behavioral_questions", []), 1):
            with st.expander(f"Behavioral Q{idx}: {q.get('question', '')}", expanded=False):
                st.caption(f"Competency: {q.get('competency', 'Leadership')}")
                st.info(f"STAR Guidance: {q.get('star_framework', '')}")


def render_outreach_module(model_choice: str, target_role: str, job_description: str) -> None:
    """Renders Module 6: Recruiter Cold Email & LinkedIn Outreach Generator."""
    st.markdown("## 📧 Recruiter Cold Email & LinkedIn Outreach Generator")
    st.markdown("Generate personalized cold emails and LinkedIn connection notes tailored to recruiters and hiring managers.")

    company_name = st.text_input("Target Company Name", placeholder="e.g. Google / Microsoft / Amazon")
    uploaded_file = st.file_uploader("Upload Resume for Context", type=["pdf", "docx"], key="outreach_uploader")

    if uploaded_file is not None:
        if st.button("🚀 Generate Outreach Messages", type="primary", use_container_width=True):
            with st.spinner("Crafting high-converting recruiter cold outreach messages..."):
                try:
                    analyzer = get_analyzer(model_choice)
                    outreach_res = analyzer.generate_outreach(uploaded_file.getvalue(), uploaded_file.name, target_role, company_name, job_description)
                    st.session_state["outreach_res"] = outreach_res
                except Exception as e:
                    st.error(f"Outreach generation error: {str(e)}")

    if "outreach_res" in st.session_state:
        o_data = st.session_state["outreach_res"]
        st.markdown("---")

        r_email = o_data.get("recruiter_email", {})
        st.markdown("### 📩 Recruiter Cold Email Template")
        st.text_input("Subject Line", value=r_email.get("subject", ""), key="rec_subj")
        st.text_area("Email Body", value=r_email.get("body", ""), height=220, key="rec_body")

        h_email = o_data.get("hiring_manager_email", {})
        st.markdown("### 👔 Hiring Manager Direct Outreach Email")
        st.text_input("Subject Line", value=h_email.get("subject", ""), key="hm_subj")
        st.text_area("Email Body", value=h_email.get("body", ""), height=220, key="hm_body")

        st.markdown("### 💬 LinkedIn Connection Note (< 300 chars)")
        st.code(o_data.get("linkedin_note", ""), language="markdown")


def render_salary_estimator_module(model_choice: str, target_role: str) -> None:
    """Renders Module 7: Salary & Compensation Range Estimator."""
    st.markdown("## 💼 Salary & Compensation Range Estimator")
    st.markdown("Estimate market compensation ranges and key negotiation leverage points based on your technical skills.")

    uploaded_file = st.file_uploader("Upload Resume for Salary Estimation", type=["pdf", "docx"], key="salary_uploader")

    if uploaded_file is not None:
        if st.button("💰 Estimate Market Salary Range", type="primary", use_container_width=True):
            with st.spinner("Analyzing market compensation data..."):
                try:
                    analyzer = get_analyzer(model_choice)
                    sal_res = analyzer.estimate_salary(uploaded_file.getvalue(), uploaded_file.name, target_role)
                    st.session_state["salary_res"] = sal_res
                except Exception as e:
                    st.error(f"Salary estimation error: {str(e)}")

    if "salary_res" in st.session_state:
        s_data = st.session_state["salary_res"]
        st.markdown("---")
        st.markdown(f"### 🏷️ Assessed Seniority Tier: `{s_data.get('seniority_level', 'Mid-Level')}`")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Estimated Min Base", f"${s_data.get('estimated_min_usd', 0):,} / yr")
        with c2:
            st.metric("Estimated Median Base", f"${s_data.get('estimated_median_usd', 0):,} / yr")
        with c3:
            st.metric("Estimated Max Base", f"${s_data.get('estimated_max_usd', 0):,} / yr")

        st.markdown("#### 🌟 Top Value-Driving Skills")
        for skill in s_data.get("top_value_skills", []):
            st.markdown(f"• `{skill}`")

        st.markdown("#### 💡 Salary Negotiation Leverage Points")
        for p in s_data.get("negotiation_leverage_points", []):
            st.info(f"✔️ {p}")


# -----------------------------------------------------------------------------
# Main Application Flow
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Main Application Flow
# -----------------------------------------------------------------------------

def main() -> None:
    """Main application flow execution."""
    module_nav, target_role, job_description, model_choice = render_sidebar()

    # Top Announcement Pill Bar
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 12px;">
            <span style="background: rgba(99, 102, 241, 0.12); border: 1px solid rgba(99, 102, 241, 0.3); color: #A5B4FC; font-size: 0.82rem; font-weight: 600; padding: 6px 18px; border-radius: 30px; display: inline-block;">
                ✨ Powered by Gemini 2.5 AI • Complete Resume Intelligence Suite
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # App Header with Logo
    col_logo, col_title = st.columns([1, 10])
    with col_logo:
        if os.path.exists("assets/logo.svg"):
            st.image("assets/logo.svg", width=76)
    with col_title:
        st.markdown('<div class="hero-title">AI Resume Analyzer ⚡</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="hero-subtitle">Optimize ATS Scores • Tailor Cover Letters • Rewrite Bullets • Predict Interview Questions • Estimate Salaries</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div style="display: flex; gap: 12px; align-items: center; margin-bottom: 1.5rem; flex-wrap: wrap;">
            <span class="trust-badge" style="margin-bottom: 0;">🔒 100% In-Memory Processing & Privacy Guarantee</span>
            <span class="trust-badge" style="margin-bottom: 0; background: rgba(99, 102, 241, 0.08); border-color: rgba(99, 102, 241, 0.25); color: #A5B4FC;">⚡ Multi-Model Fallback Engine</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Feature Grid Banner
    st.markdown(
        """
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-bottom: 2rem;">
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 16px; padding: 20px; backdrop-filter: blur(10px);">
                <div style="font-size: 1.3rem; margin-bottom: 6px;">📊 100-Point ATS Audit</div>
                <div style="color: #94A3B8; font-size: 0.88rem;">Itemized rubric scoring across formatting, hard skills, metrics, & experience.</div>
            </div>
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(168, 85, 247, 0.2); border-radius: 16px; padding: 20px; backdrop-filter: blur(10px);">
                <div style="font-size: 1.3rem; margin-bottom: 6px;">📝 Tailored Cover Letters</div>
                <div style="color: #94A3B8; font-size: 0.88rem;">Craft bespoke 3-paragraph executive cover letters from target job postings.</div>
            </div>
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(236, 72, 153, 0.2); border-radius: 16px; padding: 20px; backdrop-filter: blur(10px);">
                <div style="font-size: 1.3rem; margin-bottom: 6px;">⚡ Google XYZ Bullet Rewriter</div>
                <div style="color: #94A3B8; font-size: 0.88rem;">Rewrite weak bullet points into high-impact, quantified achievement statements.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if module_nav == "📊 AI Resume Analyzer":
        uploaded_file = st.file_uploader(
            "Upload your Resume (PDF or DOCX)",
            type=["pdf", "docx"],
            help="Supported formats: .pdf, .docx. Maximum file size: 5MB",
        )

        demo_sample_text = st.session_state.get("demo_sample_text")
        demo_sample_name = st.session_state.get("demo_sample_name")
        demo_sample_jd = st.session_state.get("demo_sample_jd")

        if uploaded_file is not None:
            file_source = uploaded_file.getvalue()
            filename = uploaded_file.name
            st.success(f"File uploaded successfully: `{filename}` ({len(file_source)/1024:.1f} KB)")
        elif demo_sample_text:
            file_source = demo_sample_text
            filename = demo_sample_name
            if not job_description:
                job_description = demo_sample_jd
            st.info(f"Loaded Sample Resume: `{filename}`")
        else:
            file_source = None
            filename = ""

        if file_source is not None:
            if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
                with st.spinner("Processing document & running AI evaluation..."):
                    try:
                        analyzer = get_analyzer(model_choice)
                        result = analyzer.analyze(file_source, filename, target_role, job_description)
                        st.session_state["analysis_result"] = result
                    except Exception as e:
                        st.error(f"Analysis Error: {str(e)}")

        if "analysis_result" in st.session_state:
            render_resume_analyzer_dashboard(st.session_state["analysis_result"])

    elif module_nav == "📝 Cover Letter Generator":
        render_cover_letter_module(model_choice, target_role, job_description)

    elif module_nav == "⚡ Bullet Point Enhancer":
        render_bullet_enhancer_module(model_choice, target_role)

    elif module_nav == "🆚 Resume A/B Comparison":
        render_ab_tester_module(model_choice, target_role, job_description)

    elif module_nav == "🎯 Resume Interview Predictor":
        render_mock_predictor_module(model_choice, target_role, job_description)

    elif module_nav == "📧 Recruiter Outreach Generator":
        render_outreach_module(model_choice, target_role, job_description)

    elif module_nav == "💼 Salary & Readiness Estimator":
        render_salary_estimator_module(model_choice, target_role)

    # Production Footer
    st.markdown(
        """
        <div class="footer">
            AI Resume Analyzer ⚡ v2.5.0<br/>
            Engineered with Python 3.13, Streamlit & Google Gemini API • MIT License
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
