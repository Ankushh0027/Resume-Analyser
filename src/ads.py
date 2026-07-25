"""
Advertisement & Sponsor Banner Engine for ResumeAI Platform
Supports dynamic top banner ads, sidebar promo widgets, and dashboard affiliate cards.
Ad settings can be managed via Admin Panel or environment variables.
"""

import os
from typing import Any
import streamlit as st

DEFAULT_AD_CONFIG = {
    "enabled": False,
    "headline": "🚀 Supercharge Your Career & Resume",
    "description": "Featured Partner: Get 1-on-1 Mock Interviews, Certified Tech Courses & Top Job Match Alerts.",
    "cta_text": "Explore Career Opportunities 👉",
    "target_url": "https://google.com",
    "banner_image": "",
    "badge_tag": "SPONSORED",
}


def get_ad_config() -> dict[str, Any]:
    """Retrieves current ad configuration from session state or environment."""
    if "ad_config" not in st.session_state:
        st.session_state["ad_config"] = {
            "enabled": os.getenv("ENABLE_ADS", "false").lower() == "true",
            "headline": os.getenv("AD_HEADLINE", DEFAULT_AD_CONFIG["headline"]),
            "description": os.getenv("AD_DESCRIPTION", DEFAULT_AD_CONFIG["description"]),
            "cta_text": os.getenv("AD_CTA_TEXT", DEFAULT_AD_CONFIG["cta_text"]),
            "target_url": os.getenv("AD_TARGET_URL", DEFAULT_AD_CONFIG["target_url"]),
            "badge_tag": os.getenv("AD_BADGE_TAG", DEFAULT_AD_CONFIG["badge_tag"]),
        }
    return st.session_state["ad_config"]


def render_top_ad_banner() -> None:
    """Renders a prominent glassmorphism Top Sponsor Banner on the main app page."""
    config = get_ad_config()
    if not config.get("enabled", False):
        return

    headline = config.get("headline", DEFAULT_AD_CONFIG["headline"])
    desc = config.get("description", DEFAULT_AD_CONFIG["description"])
    cta = config.get("cta_text", DEFAULT_AD_CONFIG["cta_text"])
    url = config.get("target_url", DEFAULT_AD_CONFIG["target_url"])
    badge = config.get("badge_tag", "SPONSORED")

    st.markdown(
        f"""
        <div class="glass-card" style="padding: 16px 20px; border-left: 4px solid #F59E0B; background: rgba(245, 158, 11, 0.08); margin: 14px 0; border-radius: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                <div>
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                        <span style="background: rgba(245, 158, 11, 0.2); border: 1px solid rgba(245, 158, 11, 0.4); color: #FBBF24; font-size: 0.7rem; font-weight: 800; padding: 2px 8px; border-radius: 8px; letter-spacing: 0.5px;">📢 {badge}</span>
                        <strong style="color: #F8FAFC; font-size: 0.98rem;">{headline}</strong>
                    </div>
                    <div style="color: #94A3B8; font-size: 0.85rem;">{desc}</div>
                </div>
                <div>
                    <a href="{url}" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #F59E0B, #D97706); color: white; font-weight: 700; font-size: 0.85rem; padding: 8px 16px; border-radius: 10px; text-decoration: none; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);">
                        {cta}
                    </a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_ad_widget() -> None:
    """Renders a sidebar advertisement widget."""
    config = get_ad_config()
    if not config.get("enabled", False):
        return

    headline = config.get("headline", DEFAULT_AD_CONFIG["headline"])
    desc = config.get("description", DEFAULT_AD_CONFIG["description"])
    cta = config.get("cta_text", DEFAULT_AD_CONFIG["cta_text"])
    url = config.get("target_url", DEFAULT_AD_CONFIG["target_url"])
    badge = config.get("badge_tag", "PARTNER AD")

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"""
        <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 12px; padding: 14px; text-align: center; margin-top: 10px;">
            <span style="background: rgba(245, 158, 11, 0.2); color: #FBBF24; font-size: 0.68rem; font-weight: 800; padding: 2px 8px; border-radius: 8px; text-transform: uppercase;">📢 {badge}</span>
            <div style="color: #F8FAFC; font-weight: 700; font-size: 0.9rem; margin: 8px 0 4px 0;">{headline}</div>
            <div style="color: #94A3B8; font-size: 0.78rem; margin-bottom: 10px; line-height: 1.4;">{desc}</div>
            <a href="{url}" target="_blank" style="display: block; background: #F59E0B; color: #0F172A; font-weight: 800; font-size: 0.8rem; padding: 6px 12px; border-radius: 8px; text-decoration: none;">
                {cta}
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )
