"""
Streamlit Web Application Entrypoint
AI Resume Analyzer Dashboard UI
"""

import streamlit as st
from src.config import config
from src.logger import logger
from src.analyzer import ResumeAnalyzer, AnalysisError
from src.parser import UnsupportedFileTypeError, ParsingError
from src.llm import LLMAuthenticationError

# -----------------------------------------------------------------------------
# Page Configuration & Modern Dark Glassmorphism Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer | Portfolio Edition",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling (CSS Injection)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Container Padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }

    /* Hero Header */
    .hero-title {
        font-size: 2.6rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        color: #9CA3AF;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* ATS Score Metric Display */
    .score-container {
        text-align: center;
        padding: 30px;
        border-radius: 20px;
        background: linear-gradient(145deg, rgba(30, 27, 75, 0.6), rgba(15, 23, 42, 0.8));
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    .score-number {
        font-size: 4.5rem;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 8px;
    }

    .score-high { color: #10B981; }
    .score-med { color: #F59E0B; }
    .score-low { color: #EF4444; }

    .score-label {
        font-size: 1.1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #D1D5DB;
    }

    /* Skill Badges */
    .badge {
        display: inline-block;
        padding: 6px 14px;
        margin: 4px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        letter-spacing: 0.3px;
    }

    .badge-tech {
        background: rgba(99, 102, 241, 0.15);
        color: #818CF8;
        border: 1px solid rgba(99, 102, 241, 0.4);
    }

    .badge-soft {
        background: rgba(168, 85, 247, 0.15);
        color: #C084FC;
        border: 1px solid rgba(168, 85, 247, 0.4);
    }

    .badge-missing {
        background: rgba(239, 68, 68, 0.15);
        color: #FCA5A5;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }

    /* Bullet List Cards */
    .insight-card {
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    .strength-item {
        background: rgba(16, 185, 129, 0.08);
        border-left: 4px solid #10B981;
        color: #E5E7EB;
    }

    .weakness-item {
        background: rgba(245, 158, 11, 0.08);
        border-left: 4px solid #F59E0B;
        color: #E5E7EB;
    }

    .suggestion-item {
        background: rgba(99, 102, 241, 0.08);
        border-left: 4px solid #6366F1;
        color: #E5E7EB;
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


def render_sidebar() -> str:
    """Renders application sidebar for user controls and settings."""
    with st.sidebar:
        st.markdown("### ⚙️ Settings & Context")

        # Target Job Role Context
        target_role = st.text_input(
            "Target Job Title (Optional)",
            placeholder="e.g., Senior Full Stack Developer",
            help="Providing a target role improves keyword alignment and missing skill detection.",
        )

        st.markdown("---")
        st.markdown("### 🔑 System Status")

        # API Key Status indicator
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

        st.markdown("---")
        st.markdown(
            """
            **About AI Resume Analyzer**
            - **Model**: `Gemini 2.5 Flash`
            - **Supported Formats**: PDF, DOCX
            - **Privacy**: Processing is completed in-memory.
            """
        )
        return target_role


def render_dashboard(result: dict) -> None:
    """Renders structured analysis results in visual cards and tabs."""
    score = result.get("ats_score", 0)
    meta = result.get("meta", {})
    color_class = get_score_color_class(score)

    st.markdown("## 📊 Analysis Dashboard")

    # Header Stats Row
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

    with col_meta:
        st.markdown("### 📝 Executive Summary")
        st.info(result.get("summary", "No summary generated."))

        # Quick file metadata stats
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Document Name", meta.get("filename", "N/A"))
        with c2:
            st.metric("Character Count", f"{meta.get('char_count', 0):,} chars")

    st.markdown("---")

    # Detailed Analysis Tabs
    tab_skills, tab_swot, tab_action = st.tabs(
        ["🎯 Skills Assessment", "⚡ Strengths & Weaknesses", "🚀 Action Plan & Suggestions"]
    )

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


def main() -> None:
    """Main application flow execution."""
    # App Header
    st.markdown('<div class="hero-title">AI Resume Analyzer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Production-grade ATS scoring, skill gap detection, and executive evaluation powered by Gemini AI</div>',
        unsafe_allow_html=True,
    )

    # Render Sidebar
    target_role = render_sidebar()

    # File Uploader Widget
    uploaded_file = st.file_uploader(
        "Upload your Resume (PDF or DOCX)",
        type=["pdf", "docx"],
        help="Supported formats: .pdf, .docx. Maximum file size: 5MB",
    )

    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        filename = uploaded_file.name

        st.success(f"File uploaded successfully: `{filename}` ({len(file_bytes)/1024:.1f} KB)")

        # Analyze Button
        if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
            with st.spinner("Processing document & running AI evaluation..."):
                try:
                    # Check session key if configured in sidebar
                    custom_key = st.session_state.get("custom_api_key")
                    analyzer = ResumeAnalyzer()
                    if custom_key:
                        from src.llm import GeminiClient
                        analyzer.llm_client = GeminiClient(api_key=custom_key)

                    # Trigger Analysis Pipeline
                    result = analyzer.analyze(
                        file_source=file_bytes,
                        filename=filename,
                        target_role=target_role,
                    )

                    # Store result in session state
                    st.session_state["analysis_result"] = result

                except UnsupportedFileTypeError as e:
                    st.error(f"Invalid file format: {str(e)}")
                except ParsingError as e:
                    st.error(f"Text extraction failed: {str(e)}")
                except LLMAuthenticationError as e:
                    st.error(f"Authentication Error: {str(e)}")
                except AnalysisError as e:
                    st.error(f"Analysis failed: {str(e)}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {str(e)}")
                    logger.error(f"Unhandled Streamlit UI exception: {str(e)}", exc_info=True)

    # Render existing analysis result from session state if available
    if "analysis_result" in st.session_state:
        render_dashboard(st.session_state["analysis_result"])


if __name__ == "__main__":
    main()
