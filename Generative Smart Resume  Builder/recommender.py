from datetime import date

import numpy as np
import pandas as pd
import streamlit as st
import torch
from sentence_transformers import SentenceTransformer

from models.model import TwoTowerVAE


# -----------------------------
# Config
# -----------------------------

SBERT_NAME = "anass1209/resume-job-matcher-all-MiniLM-L6-v2"
MODEL_VAE_PATH = "models/twotower_vae.pt"
MODEL_D_PATH = "models/D.pt"
JOBS_PATH = "models/jobs.pkl"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

MONTHS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

HIDDEN_DIM = 64
LATENT_DIM = 8

# -----------------------------
# Load resources once
# -----------------------------

@st.cache_resource
def load_sbert():
    """Load SBERT model once."""
    return SentenceTransformer(SBERT_NAME)

@st.cache_resource
def load_vae(input_dim):
    """Load trained TwoTowerVAE model."""
    model = TwoTowerVAE(
        input_dim,
        input_dim,
        hidden_dim=HIDDEN_DIM,
        latent_dim=LATENT_DIM,
    )

    state = torch.load(MODEL_VAE_PATH, map_location=DEVICE)
    model.load_state_dict(state, strict=True)
    model.to(DEVICE)
    model.eval()

    return model


@st.cache_data
def load_jobs():
    """Load jobs dataframe and convert job embeddings to numpy float32 arrays."""
    jobs = pd.read_pickle(JOBS_PATH)
    jobs["job_emb"] = jobs["job_emb"].apply(lambda x: np.asarray(x, dtype=np.float32))
    return jobs


def load_recommendation_resources():
    """Load all recommendation resources used by the app."""
    jobs_df = load_jobs()
    sbert = load_sbert()
    job_dim = int(jobs_df["job_emb"].iloc[0].shape[0])
    vae = load_vae(job_dim)
    return jobs_df, sbert, vae


# -----------------------------
# Experience helpers
# -----------------------------

def month_year_to_date(month_str: str, year: int) -> date:
    m = MONTHS.index(month_str) + 1
    return date(int(year), m, 1)


def months_between(start: date, end: date) -> int:
    if end < start:
        return 0
    return (end.year - start.year) * 12 + (end.month - start.month)


def merge_intervals(intervals):
    """Merge overlapping work experience periods."""
    if not intervals:
        return []

    intervals = sorted(intervals, key=lambda x: x[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return merged


def total_experience_years(experiences) -> float:
    """Calculate total work experience in years without double-counting overlaps."""
    intervals = []

    for exp in experiences:
        if not exp.get("start_month") or not exp.get("start_year"):
            continue
        if not exp.get("end_month") or not exp.get("end_year"):
            continue

        start = month_year_to_date(exp["start_month"], exp["start_year"])
        end = month_year_to_date(exp["end_month"], exp["end_year"])

        if end < start:
            continue

        intervals.append((start, end))

    total_months = sum(months_between(start, end) for start, end in merge_intervals(intervals))
    return total_months / 12.0


def experience_bucket(years: float) -> str:
    if years < 1:
        return "Less than 1 year"
    if years < 2:
        return "1 to 2 years"
    if years < 3:
        return "2 to 3 years"
    if years < 5:
        return "3 to 5 years"
    return "More than 5 years"

# -----------------------------
# Text helpers
# -----------------------------

def normalize_for_embedding(text: str) -> str:
    if text is None:
        return ""
    return text.strip().lower()


def normalize_skills_csv(skills_csv: str):
    """Convert comma-separated skills into a clean, lowercase, unique list."""
    items = [s.strip().lower() for s in (skills_csv or "").split(",") if s.strip()]

    seen = set()
    output = []
    for item in items:
        if item not in seen:
            seen.add(item)
            output.append(item)

    return output


def combined_skills(skills, experiences):
    """Combine main skills and experience skills into one unique list."""
    global_skills = normalize_skills_csv(skills)

    company_skills = []
    for exp in experiences:
        company_skills.extend(normalize_skills_csv(exp.get("company_skills", "")))

    seen = set()
    output = []
    for skill in global_skills + company_skills:
        if skill not in seen:
            seen.add(skill)
            output.append(skill)

    return output


def clean_education_list(education_list):
    return [item.strip() for item in education_list if item and item.strip()]


# -----------------------------
# Candidate text builder
# -----------------------------

def build_candidate_text(career_objective, skills, education_list, major, experiences):
    """Build structured candidate text for SBERT embedding."""
    edu_items = [e.strip().lower() for e in education_list if e and e.strip()]
    edu_str = ", ".join(edu_items) or "n/a"

    combine_skills = ", ".join(combined_skills(skills, experiences)) or "n/a"
    major_str = (major or "").strip().lower() or "n/a"
    years = total_experience_years(experiences)
    exp_str = experience_bucket(years).lower()
    career_obj_str = normalize_for_embedding(career_objective) or "n/a"

    return (
        f"career objective: {career_obj_str}\n"
        f"skills: {combine_skills}\n"
        f"education: {edu_str}\n"
        f"major: {major_str}\n"
        f"experience: {exp_str}\n"
    )


# -----------------------------
# Scoring functions
# -----------------------------

@torch.no_grad()
def score_jobs_vae(vae_model, cand_emb, job_emb_matrix):
    xc = torch.from_numpy(cand_emb).float().to(DEVICE).unsqueeze(0)
    xj = torch.from_numpy(job_emb_matrix).float().to(DEVICE)
    xc_rep = xc.repeat(xj.shape[0], 1)
    out = vae_model(xc_rep, xj)
    y_hat = out[-1].squeeze(1)
    return y_hat.detach().cpu().numpy()

def recommend_jobs(jobs_df, sbert,vae, top_n, career_objective, skills, education_list, major, experiences):
    """Generate ranked job recommendations and return recommendations plus candidate text."""
    cand_text = build_candidate_text(
        career_objective=career_objective,
        skills=skills,
        education_list=education_list,
        major=major,
        experiences=experiences,
    )

    cand_emb = sbert.encode([cand_text], normalize_embeddings=False)[0].astype(np.float32)
    job_emb_matrix = np.stack(jobs_df["job_emb"].values).astype(np.float32)

    scores = score_jobs_vae(vae, cand_emb, job_emb_matrix)
    recs = jobs_df.copy()
    recs["pred_score"] = scores
    recs = recs.sort_values("pred_score", ascending=False).head(int(top_n)).reset_index(drop=True)

    return recs, cand_text
