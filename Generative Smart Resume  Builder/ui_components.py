from html import escape

import streamlit as st

from recommender import combined_skills


def apply_custom_css():
    st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2.5rem;
    max-width: 1300px;
}

.hero-section {
    padding: 28px 32px;
    border-radius: 24px;
    background: linear-gradient(135deg, #111827 0%, #1e3a8a 55%, #2563eb 100%);
    border: 1px solid #374151;
    margin-bottom: 28px;
    box-shadow: 0 18px 45px rgba(0, 0, 0, 0.22);
}

.hero-section h1 {
    font-size: 46px;
    font-weight: 850;
    margin-bottom: 6px;
    color: #f9fafb;
    letter-spacing: -0.03em;
}

.hero-section p {
    font-size: 18px;
    color: #dbeafe;
    margin-bottom: 0;
}

.section-title {
    font-size: 20px;
    font-weight: 800;
    color: #f9fafb;
    margin-bottom: 12px;
}

.section-caption {
    color: #9ca3af;
    font-size: 14px;
    margin-top: -6px;
    margin-bottom: 16px;
}

.info-card {
    padding: 18px 20px;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(30, 58, 138, 0.55), rgba(15, 23, 42, 0.9));
    border: 1px solid rgba(59, 130, 246, 0.35);
    margin-bottom: 16px;
}

.info-card strong {
    color: #f9fafb;
}

.info-card span {
    color: #bfdbfe;
}

.resume-preview {
    padding: 28px;
    border-radius: 20px;
    background-color: #f9fafb;
    color: #111827;
    border: 1px solid #e5e7eb;
    min-height: 520px;
    box-shadow: 0 14px 36px rgba(0, 0, 0, 0.20);
}

.resume-preview h2 {
    font-size: 30px;
    font-weight: 850;
    color: #111827;
    margin-bottom: 2px;
    letter-spacing: -0.02em;
}

.resume-preview .role-line {
    color: #2563eb;
    font-weight: 700;
    margin-bottom: 12px;
}

.resume-preview h3 {
    font-size: 15px;
    font-weight: 850;
    color: #1e40af;
    border-bottom: 1px solid #d1d5db;
    padding-bottom: 5px;
    margin-top: 20px;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.resume-preview p,
.resume-preview li {
    font-size: 14px;
    color: #374151;
    line-height: 1.55;
}

.skill-pill {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    background: #dbeafe;
    color: #1e3a8a;
    font-size: 12px;
    font-weight: 700;
    margin: 3px 4px 3px 0;
}

.job-card {
    padding: 18px 20px;
    border-radius: 18px;
    background-color: rgba(17, 24, 39, 0.88);
    border: 1px solid rgba(75, 85, 99, 0.9);
    margin-bottom: 14px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.14);
}

.job-title {
    font-size: 17px;
    font-weight: 800;
    color: #f9fafb;
    margin-bottom: 4px;
}

.job-score {
    color: #93c5fd;
    font-size: 13px;
    font-weight: 650;
}

.stButton > button {
    border-radius: 13px;
    height: 48px;
    font-weight: 800;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stNumberInput"] input {
    border-radius: 12px;
}

div[role="radiogroup"] label {
    padding-right: 14px;
}
</style>
""", unsafe_allow_html=True)


def render_header():
    st.markdown("""
<div class="hero-section">
    <h1>Generative Smart Resume Builder</h1>
    <p>AI-powered resume builder and job recommendation system</p>
</div>
""", unsafe_allow_html=True)


def section_title(title: str, caption: str | None = None):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if caption:
        st.markdown(f'<div class="section-caption">{caption}</div>', unsafe_allow_html=True)

def render_job_cards(recs):
    st.markdown("### 🎯 Recommended Jobs")

    for idx, row in recs.iterrows():
        job_name = escape(str(row.get("job_name", "Unknown Job")))
        score = float(row.get("pred_score", 0.0))

        st.markdown(f"""
<div class="job-card">
    <div class="job-title">{idx + 1}. {job_name}</div>
</div>
""", unsafe_allow_html=True)
