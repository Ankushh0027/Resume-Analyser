"""
Authentication Module for AI Resume Analyzer SaaS
Manages user session state, registration, login, and default demo user session binding.
"""

import streamlit as st
from typing import Any
from src.database import authenticate_user, register_user, seed_demo_user, get_user_usage


def get_current_user() -> dict[str, Any] | None:
    """Returns currently logged in user dictionary from Streamlit session_state."""
    return st.session_state.get("user")


def login_as_demo_user() -> dict[str, Any]:
    """Explicitly logs in as demo user for instant evaluation."""
    demo_user = seed_demo_user()
    st.session_state["user"] = demo_user
    return demo_user


def login_user(email: str, password: str) -> tuple[bool, str]:
    """Authenticates user and binds session state."""
    user = authenticate_user(email, password)
    if user:
        st.session_state["user"] = user
        return True, f"Welcome back, {user['name']}!"
    return False, "Invalid email or password."


def signup_user(email: str, name: str, password: str) -> tuple[bool, str]:
    """Registers new user account and binds session state."""
    try:
        user = register_user(email, name, password)
        st.session_state["user"] = user
        return True, f"Account created! Welcome, {name}."
    except Exception as e:
        return False, str(e)


def logout_user() -> None:
    """Logs out current user and resets session state."""
    st.session_state["user"] = None
    if "analysis_result" in st.session_state:
        del st.session_state["analysis_result"]
    if "cl_result" in st.session_state:
        del st.session_state["cl_result"]


def render_login_screen() -> None:
    """Renders a dedicated, high-converting glassmorphism login & sign-up portal."""
    st.markdown(
        """
        <div style="max-width: 680px; margin: 30px auto 20px auto; text-align: center;">
            <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(129, 140, 248, 0.4); border-radius: 20px; padding: 4px 16px; margin-bottom: 12px;">
                <span style="color: #818CF8; font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px;">⚡ Enterprise Career Intelligence</span>
            </div>
            <div class="hero-title" style="font-size: 2.6rem; background: linear-gradient(135deg, #F8FAFC 30%, #818CF8 70%, #C084FC 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                AI Resume Analyzer & Career Suite
            </div>
            <p style="color: #94A3B8; font-size: 1.05rem; margin-top: 10px; line-height: 1.6;">
                Engineered for tech professionals. Get instant ATS scoring, market-adjusted salary benchmarks, cover letter generation, and recruiter outreach.
            </p>
            <div style="display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; margin-top: 16px;">
                <span style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3); color: #34D399; font-size: 0.8rem; font-weight: 600; padding: 4px 12px; border-radius: 14px;">🎯 98% ATS Accuracy</span>
                <span style="background: rgba(99, 102, 241, 0.12); border: 1px solid rgba(129, 140, 248, 0.3); color: #A5B4FC; font-size: 0.8rem; font-weight: 600; padding: 4px 12px; border-radius: 14px;">💼 Regional Salary Engine</span>
                <span style="background: rgba(245, 158, 11, 0.12); border: 1px solid rgba(245, 158, 11, 0.3); color: #FBBF24; font-size: 0.8rem; font-weight: 600; padding: 4px 12px; border-radius: 14px;">📧 Executive Outreach</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c_center = st.columns([1, 2, 1])[1]
    with c_center:
        st.markdown('<div class="glass-card" style="padding: 28px;">', unsafe_allow_html=True)
        tab_login, tab_signup = st.tabs(["🔑 Log In", "✨ Create Account"])

        with tab_login:
            st.markdown("### Welcome Back")
            email = st.text_input("Email Address", key="main_login_email", placeholder="user@company.com")
            password = st.text_input("Password", type="password", key="main_login_pwd", placeholder="••••••••")

            if st.button("🚀 Sign In to Account", type="primary", use_container_width=True, key="main_login_btn"):
                if not email or not password:
                    st.error("Please fill in both email and password.")
                else:
                    with st.spinner("Authenticating credentials..."):
                        ok, msg = login_user(email, password)
                        if ok:
                            st.toast(msg, icon="🎉")
                            st.rerun()
                        else:
                            st.error(msg)

        with tab_signup:
            st.markdown("### Create Free Account")
            name = st.text_input("Full Name", key="main_signup_name", placeholder="Alex Johnson")
            email = st.text_input("Email Address", key="main_signup_email", placeholder="alex@company.com")
            password = st.text_input("Password", type="password", key="main_signup_pwd", placeholder="Minimum 6 characters")

            if st.button("✨ Create Free Account", type="primary", use_container_width=True, key="main_signup_btn"):
                if not name or not email or not password:
                    st.error("Please complete all registration fields.")
                elif len(password.strip()) < 4:
                    st.error("Password should be at least 4 characters long.")
                else:
                    with st.spinner("Creating your account & setting up workspace..."):
                        ok, msg = signup_user(email, name, password)
                        if ok:
                            st.toast(msg, icon="🎉")
                            st.rerun()
                        else:
                            st.error(msg)

        st.markdown("</div>", unsafe_allow_html=True)


def render_auth_header() -> bool:
    """
    Renders top production header bar.
    Returns True if login portal is triggered, False otherwise.
    """
    user = get_current_user()

    if user:
        badge_html = '<span style="background: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.5); color: #A7F3D0; font-weight: 700; font-size: 0.82rem; padding: 6px 14px; border-radius: 20px;">⚡ Unlimited Platform Access</span>'

        c1, c2, c3 = st.columns([6, 3, 2])
        with c1:
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 12px; padding: 4px 0;">
                    <span style="font-weight: 800; font-size: 1.15rem; color: #F8FAFC;">⚡ ResumeAI</span>
                    <span style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); color: #34D399; font-weight: 600; font-size: 0.78rem; padding: 2px 10px; border-radius: 12px;">🟢 Online</span>
                    <span style="color: #94A3B8; font-size: 0.9rem;">| &nbsp;👤 <strong>{user['name']}</strong></span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f"""
                <div style="text-align: right; padding: 4px 0;">
                    {badge_html}
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c3:
            if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
                logout_user()
                st.session_state["show_auth_portal"] = False
                st.session_state["show_pricing_modal"] = False
                st.rerun()
        return False
    else:
        c1, c2 = st.columns([8, 2])
        with c1:
            st.markdown(
                """
                <div style="display: flex; align-items: center; gap: 12px; padding: 4px 0;">
                    <span style="font-weight: 800; font-size: 1.15rem; color: #F8FAFC;">⚡ ResumeAI</span>
                    <span style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); color: #34D399; font-weight: 600; font-size: 0.78rem; padding: 2px 10px; border-radius: 12px;">🟢 System Online</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c2:
            if st.button("🔑 Log In / Sign Up", key="hdr_login_btn", type="primary", use_container_width=True):
                st.session_state["show_auth_portal"] = True
                st.rerun()

        return bool(st.session_state.get("show_auth_portal", False))
