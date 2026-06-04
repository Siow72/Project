from datetime import date

import streamlit as st

from recommender import (
    MONTHS,
    load_recommendation_resources,
    recommend_jobs,
)

from ui_components import (
    apply_custom_css,
    render_header,
    render_job_cards,
    section_title,
)

from resume_builder import render_resume_builder_page

#-------------------------
# Helper Function
#-------------------------

# avoid empty value
def get_default_education():
    return {
        "degree": "",
        "industry": "",
        "start_month": "Jan",
        "start_year": date.today().year,
        "end_month": "Jan",
        "end_year": date.today().year,
        "currently_studying": False,
        "include_cgpa": False,
        "cgpa": 3.00,
    }

def get_default_experience():
    return {
        "company": "",
        "company_skills": "",
        "achievement": "",
        "position": "",
        "start_month": "Jan",
        "start_year": date.today().year,
        "end_month": "Jan",
        "end_year": date.today().year,
    }


# function to avoid empty value and invalid format
def normalize_education(edu):
    default_edu = get_default_education()

    if isinstance(edu, str):
        default_edu["degree"] = edu
        return default_edu

    if isinstance(edu, dict):
        for key, value in default_edu.items():
            edu.setdefault(key, value)
        return edu

    return default_edu

# find the position on the MONTHS and prevent invalid month
def get_month_index(month):
    if month in MONTHS:
        return MONTHS.index(month)
    return MONTHS.index("Jan")

# extract degree name from the education list for job recommendation purpose 
def format_education_for_recommendation(edu):
    parts = []

    if edu.get("degree"):
        parts.append(edu["degree"])

    return " | ".join(parts)


# -----------------------------
# Page setup
# -----------------------------

st.set_page_config(
    page_title="Generative Smart Resume Builder",
    page_icon="✨",
    layout="wide",
)

apply_custom_css()


# -----------------------------
# Session defaults
# -----------------------------

# use for store information
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "Job Recommendation"

if "job_recommendation_done" not in st.session_state:
    st.session_state["job_recommendation_done"] = False

if "selected_job" not in st.session_state:
    st.session_state["selected_job"] = None

if "candidate_profile" not in st.session_state:
    st.session_state["candidate_profile"] = {}

if "education_list" not in st.session_state:
    st.session_state["education_list"] = [get_default_education()]

# Convert old education format into the new dictionary format
st.session_state["education_list"] = [
    normalize_education(edu)
    for edu in st.session_state["education_list"]
]

if "experiences" not in st.session_state:
    st.session_state["experiences"] = [get_default_experience()]


# -----------------------------
# Sidebar navigation
# -----------------------------

pages = ["Job Recommendation", "Resume Builder"]

st.sidebar.radio(
    "Navigation",
    pages,
    key="active_page",
)


# -----------------------------
# Header
# -----------------------------

render_header()


# -----------------------------
# Page 1: Job Recommendation
# -----------------------------

if st.session_state["active_page"] == "Job Recommendation":

    with st.spinner("Loading AI models and job data..."):
        #load the resource
        jobs_df, sbert, vae = load_recommendation_resources()

    left, right = st.columns([1.28, 1], gap="large")

    # -----------------------------
    # Left column: user input
    # -----------------------------

    with left:
        section_title(
            "👤 Candidate Profile",
            "Enter your details for job matching.",
        )

        career_objective = st.text_area(
            "Career Goal / Professional Objective",
            height=95,
            placeholder="Example: I am an IT graduate interested in data analysis and business intelligence.",
        )

        c1, c2 = st.columns([1, 1])

        with c1:
            skills = st.text_input(
                "Key Skills",
                placeholder="Example: Python, SQL",
            )

        with c2:
            major = st.text_input(
                "Field of Study",
                placeholder="Example: Data Science, Finance",
            )

        st.divider()

        # -----------------------------
        # Education
        # -----------------------------

        section_title("🎓 Education")

        for i, edu in enumerate(st.session_state["education_list"]):
            with st.expander(f"Education #{i + 1}", expanded=True):

                c1, c2 = st.columns([1, 1])

                with c1:
                    edu["degree"] = st.text_input(
                        f"Degree #{i + 1}",
                        value=edu.get("degree", ""),
                        placeholder="Example: Bachelor of Information Technology",
                        key=f"edu_{i}_degree",
                    )

                with c2:
                    edu["industry"] = st.text_input(
                        "School",
                        value=edu.get("industry", ""),
                        placeholder="Example: MMU",
                        key=f"edu_{i}_industry",
                    )

                st.markdown("#### Education Period")

                p1, p2 = st.columns([1, 1])

                with p1:
                    edu["start_month"] = st.selectbox(
                        "Start Month",
                        MONTHS,
                        index=get_month_index(edu.get("start_month", "Jan")),
                        key=f"edu_{i}_start_month",
                    )

                    edu["start_year"] = st.number_input(
                        "Start Year",
                        min_value=1950,
                        max_value=date.today().year,
                        value=int(edu.get("start_year", date.today().year)),
                        step=1,
                        key=f"edu_{i}_start_year",
                    )

                with p2:
                    edu["currently_studying"] = st.checkbox(
                        "Currently studying?",
                        value=edu.get("currently_studying", False),
                        key=f"edu_{i}_currently_studying",
                    )

                    if not edu["currently_studying"]:
                        edu["end_month"] = st.selectbox(
                            "End Month",
                            MONTHS,
                            index=get_month_index(edu.get("end_month", "Jan")),
                            key=f"edu_{i}_end_month",
                        )

                        edu["end_year"] = st.number_input(
                            "End Year",
                            min_value=1950,
                            max_value=date.today().year,
                            value=int(edu.get("end_year", date.today().year)),
                            step=1,
                            key=f"edu_{i}_end_year",
                        )

                st.markdown("#### CGPA")

                edu["include_cgpa"] = st.checkbox(
                    "Add CGPA?",
                    value=edu.get("include_cgpa", False),
                    key=f"edu_{i}_include_cgpa",
                )

                if edu["include_cgpa"]:
                    edu["cgpa"] = st.number_input(
                        "CGPA",
                        min_value=0.00,
                        max_value=4.00,
                        value=float(edu.get("cgpa", 3.00)),
                        step=0.01,
                        format="%.2f",
                        key=f"edu_{i}_cgpa",
                    )

                remove_clicked = st.button(
                    "Remove this education",
                    key=f"edu_remove_{i}",
                    use_container_width=True,
                    disabled=len(st.session_state["education_list"]) <= 1,
                )

                if remove_clicked:
                    st.session_state["education_list"].pop(i)
                    st.rerun()

        if st.button("➕ Add another degree"):
            st.session_state["education_list"].append(get_default_education())
            st.rerun()

        st.divider()

        # -----------------------------
        # Work Experience
        # -----------------------------

        section_title(
            "💼 Work Experience",
        )

        for i, exp in enumerate(st.session_state["experiences"]):
            with st.expander(f"Experience #{i + 1}", expanded=True):

                c3, c4 = st.columns([1, 1])

                with c3:
                    exp["position"] = st.text_input(
                        "Position",
                        value=exp.get("position", ""),
                        placeholder="Example: Data Analyst Intern",
                        key=f"exp_{i}_position",
                    )

                with c4:
                    exp["company"] = st.text_input(
                    "Company / Organization",
                    value=exp.get("company", ""),
                    placeholder="Example: Maybank",
                    key=f"exp_{i}_company",
                )
        
                exp["company_skills"] = st.text_input(
                    "Skills Used in This Role",
                    value=exp.get("company_skills", ""),
                    placeholder="Example: Excel, financial modeling, Python",
                    key=f"exp_{i}_company_skills",
                )

                exp["achievement"] = st.text_input(
                    "Achievement",
                    value=exp.get("achievement", ""),
                    placeholder="Example: Improved reporting efficiency by 30%",
                    key=f"exp_{i}_achievement",
                )

            
                a, b = st.columns([1, 1])

                with a:
                    exp["start_month"] = st.selectbox(
                        "Start Month",
                        MONTHS,
                        index=get_month_index(exp.get("start_month", "Jan")),
                        key=f"exp_{i}_start_month",
                    )

                    exp["start_year"] = st.number_input(
                        "Start Year",
                        min_value=1950,
                        max_value=date.today().year,
                        value=int(exp.get("start_year", date.today().year)),
                        step=1,
                        key=f"exp_{i}_start_year",
                    )

                with b:
                    exp["end_month"] = st.selectbox(
                        "End Month",
                        MONTHS,
                        index=get_month_index(exp.get("end_month", "Jan")),
                        key=f"exp_{i}_end_month",
                    )

                    exp["end_year"] = st.number_input(
                        "End Year",
                        min_value=1950,
                        max_value=date.today().year,
                        value=int(exp.get("end_year", date.today().year)),
                        step=1,
                        key=f"exp_{i}_end_year",
                    )

                if (
                    st.button("Remove this experience", key=f"exp_remove_{i}")
                    and len(st.session_state["experiences"]) > 1
                ):
                    st.session_state["experiences"].pop(i)
                    st.rerun()

        if st.button("➕ Add another experience"):
            st.session_state["experiences"].append(get_default_experience())
            st.rerun()

    # -----------------------------
    # Right column: recommendation
    # -----------------------------

    with right:
        section_title("⚙️ Recommendation Settings",
                     "Max : 10 | Min : 3")

        top_n = st.number_input(
            "Number of recommendations",
            min_value=3,
            max_value=10,
            value=5,
            step=1,
        )
        recommend_clicked = st.button(
            "Generate Recommendations (Powered by VAE Model)",
            type="primary",
            use_container_width=True,
        )

        st.divider()


        if recommend_clicked:
            with st.spinner("Analyzing candidate profile and generating job recommendations..."):

                education_for_recommendation = [
                    format_education_for_recommendation(edu)
                    for edu in st.session_state["education_list"]
                ]

                
                recs, cand_text = recommend_jobs(
                    jobs_df=jobs_df,
                    sbert=sbert,
                    vae = vae,
                    top_n=top_n,
                    career_objective=career_objective,
                    skills=skills,
                    education_list=education_for_recommendation,
                    major=major,
                    experiences=st.session_state["experiences"],
                )

                st.session_state["recs"] = recs
                st.session_state["cand_text"] = cand_text
                st.session_state["candidate_profile"] = {
                    "career_objective": career_objective,
                    "skills": skills,
                    "major": major,
                    "education_details": [
                        edu.copy()
                        for edu in st.session_state["education_list"]
                    ],

                    "experiences": st.session_state["experiences"],
                }

                st.session_state["selected_job"] = None
                st.session_state["job_recommendation_done"] = False

            st.success(f"Top-{top_n} job recommendations generated using VAE!")

        if "recs" in st.session_state:
            recs = st.session_state["recs"]

            render_job_cards(recs)

            st.divider()

            st.markdown("### ✅ Select Recommended Job")

            selected_idx = st.selectbox(
                "Choose one recommended job before going to Resume Builder",
                options=list(range(len(recs))),
                format_func=lambda idx: str(recs.iloc[idx].get("job_name", "Unknown Job")),
            )

            if st.button("Confirm Selected Job", type="primary", use_container_width=True):
                selected_job = recs.iloc[selected_idx].to_dict()

                st.session_state["selected_job"] = selected_job
                st.session_state["job_recommendation_done"] = True

                st.success(
                    f"Selected job: {selected_job.get('job_name', 'Unknown Job')}. "
                    "You can now go to Resume Builder."
                )


        else:
            st.caption("Fill in the profile on the left and click **Generate Recommendations**.")


# -----------------------------
# Page 2: Resume Builder
# -----------------------------

elif st.session_state["active_page"] == "Resume Builder":
    render_resume_builder_page()