import numpy as np
import json
import time
import ollama
import io
import streamlit as st

from ui_components import section_title
from pdf_generator import generate_resume_pdf_buffer

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROMPT_PATH = BASE_DIR / "prompt.txt"
# ----------------------
# Helper Function
# ----------------------

#prevent empty or None Value
def safe_text(value, fallback=""):
    if value is None:
        return fallback
    value = str(value).strip()
    return value if value else fallback

def make_json_safe(obj):
    if isinstance(obj, dict):
        return {str(k): make_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    if isinstance(obj, tuple):
        return [make_json_safe(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if obj is None:
        return ""
    return obj


# combine start and end dates in format : Jan 2024 - Dec 2024
def build_period(start_month, start_year, end_month, end_year):
    start = " ".join(
        part for part in [
            safe_text(start_month),
            safe_text(start_year),
        ]
        if part
    )

    end = " ".join(
        part for part in [
            safe_text(end_month),
            safe_text(end_year),
        ]
        if part
    )

    if start and end:
        return f"{start} - {end}"

    return start or end

# Combine all work experience and format it into :
'''
Data Analyst Intern | Jan 2024 - Mar 2024
Maybank

- Improved reporting efficiency by 30%
- Applied skills in Python, Excel.
'''

def build_work_experience_markdown(position, company, period, bullet_points):
    md = ""

    position = safe_text(position)
    company = safe_text(company)
    period = safe_text(period)
    bullet_points = bullet_points or []

    heading_parts = []

    if position:
        heading_parts.append(position)

    if period:
        heading_parts.append(period)

    if heading_parts:
        md += f"### {' | '.join(heading_parts)}\n"

    if company:
        md += f"{company}\n"

    if heading_parts or company:
        md += "\n"

    for bullet in bullet_points:
        bullet = safe_text(bullet)
        if bullet:
            md += f"- {bullet}\n"

    md += "\n"
    return md

# function to read the education data
def parse_education_entry(edu):
    degree = ""
    institution = ""
    period = ""
    cgpa = ""

    if not isinstance(edu, dict):
        return degree, institution, period, cgpa

    degree = safe_text(edu.get("degree"))

    institution = safe_text(
        edu.get("institution")
        or edu.get("university")
        or edu.get("school")
        or edu.get("industry")
    )

    start_month = safe_text(edu.get("start_month"))
    start_year = safe_text(edu.get("start_year"))

    if edu.get("currently_studying"):
        end_month = "Present"
        end_year = ""
    else:
        end_month = safe_text(edu.get("end_month"))
        end_year = safe_text(edu.get("end_year"))

    has_education_content = degree or institution or edu.get("include_cgpa")

    if has_education_content:
        period = build_period(
            start_month=start_month,
            start_year=start_year,
            end_month=end_month,
            end_year=end_year,
        )
    else:
        period = ""

    if edu.get("include_cgpa"):
        cgpa = f"{float(edu.get('cgpa', 0.00)):.2f}"

    return degree, institution, period, cgpa

# Converts special Python/Numpy objects into normal JSON-friendly data.
    if isinstance(obj, dict):
        return {str(k): make_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    if isinstance(obj, tuple):
        return [make_json_safe(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if obj is None:
        return ""
    return obj

# default value for project and certification section
def get_default_project():
    return {
        "project_name": "",
        "project_description": "",
        "project_achievement": "",
    }


def get_default_certification():
    return {
        "cert_name": "",
        "issuer": "",
        "year": "",
    }

# function to run the ollama model
def run_ollama_model(model_name, prompt):
    start_time = time.time()

    response = ollama.chat(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert resume writer. "
                    "You generate truthful, concise, ATS-friendly resume content."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        format="json",
        options={"temperature": 0.2},
    )

    end_time = time.time()
    content = response["message"]["content"]

    try:
        output = json.loads(content)
        json_valid = True
    except json.JSONDecodeError:
        output = {"raw_output": content}
        json_valid = False

    return {
        "model_name": model_name,
        "output": output,
        "json_valid": json_valid,
        "response_time_seconds": round(end_time - start_time, 2),
    }

# main function to connect ollama
# step 1 : optn prompt.txt
# step 2 : Inserts the user data into the prompt
# step 3 :Sends it to Ollama
# step 4 :Converts the JSON result into resume Markdown
# model used : llama3.2:3b
def generate_resume_with_ollama(prompt_file, llm_resume_input):
    try:
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt_template = f.read()

        input_json = json.dumps(
            make_json_safe(llm_resume_input),
            indent=2,
            ensure_ascii=False,
        )

        final_prompt = prompt_template.replace("{input_json}", input_json)

        result = run_ollama_model(
            model_name="llama3.2:3b",
            prompt=final_prompt,
        )

        if not result["json_valid"]:
            return result["output"].get("raw_output", "")

        return convert_json_to_markdown(result["output"], llm_resume_input)

    except Exception as e:
        st.error(f"Ollama error: {e}")
        return ""

# Converts Ollama’s JSON output into resume text.
def convert_json_to_markdown(output, original_input=None):
    resume_md = ""
    original_input = original_input or {}

    summary = output.get("summary", "")
    if summary:
        resume_md += "## Professional Summary\n\n"
        resume_md += summary + "\n"

    hard_skills = output.get("hard_skills", [])
    soft_skills = output.get("soft_skills", [])

    if hard_skills or soft_skills:
        resume_md += "\n\n---\n\n## Skills\n\n"

        if hard_skills:
            resume_md += "### Hard Skills\n"
            for skill in hard_skills:
                resume_md += f"- {skill}\n"

        if soft_skills:
            resume_md += "\n### Soft Skills\n"
            for skill in soft_skills:
                resume_md += f"- {skill}\n"

    generated_projects = output.get("project_section", [])
    original_projects = original_input.get("projects", [])

    if generated_projects or original_projects:
        resume_md += "\n\n---\n\n## Project Experience\n\n"

        project_count = max(len(generated_projects), len(original_projects))

        for i in range(project_count):
            project = generated_projects[i] if i < len(generated_projects) else {}
            original_project = original_projects[i] if i < len(original_projects) else {}

            project_name = original_project.get(
                "project_name",
                project.get("project_name", ""),
            )

            bullet_points = project.get("bullet_points", [])

            if project_name:
                resume_md += f"### {project_name}\n\n"

            for bullet in bullet_points:
                resume_md += f"- {bullet}\n"

            resume_md += "\n"

    generated_experiences = output.get("experience_section", [])
    original_experiences = original_input.get("experiences", [])

    if generated_experiences or original_experiences:
        resume_md += "\n\n---\n\n## Work Experience\n\n"

        experience_count = max(len(generated_experiences), len(original_experiences))

        for i in range(experience_count):
            exp = generated_experiences[i] if i < len(generated_experiences) else {}
            original_exp = original_experiences[i] if i < len(original_experiences) else {}

            position = original_exp.get("position", exp.get("position", ""))
            company = original_exp.get("company", exp.get("company", ""))

            start_month = original_exp.get("start_month", "")
            start_year = original_exp.get("start_year", "")
            end_month = original_exp.get("end_month", "")
            end_year = original_exp.get("end_year", "")

            period = build_period(
                start_month=start_month,
                start_year=start_year,
                end_month=end_month,
                end_year=end_year,
            )

            bullet_points = exp.get("bullet_points", [])

            resume_md += build_work_experience_markdown(
                position=position,
                company=company,
                period=period,
                bullet_points=bullet_points,
            )

    return resume_md.strip()

# Build information on the text box
def build_private_header(full_name, email, phone, location, profile_links):
    return f"""
# {safe_text(full_name, "Your Name")}

**Location:** {safe_text(location, "Your location")}  
**Email:** {safe_text(email, "your.email@example.com")}  
**Phone:** {safe_text(phone, "Your phone number")}  

**Profile Links:**  
{profile_links}
""".strip()

# Builds the Education section from education_list.
def build_original_education_markdown(education_list):
  
    if not education_list:
        return "\n\n---\n\n## Education\n\nNo education provided.\n"

    md = "\n\n---\n\n## Education\n\n"
    has_education = False

    for edu in education_list:
        degree, institution, period, cgpa = parse_education_entry(edu)

        if degree or institution or period or cgpa:
            has_education = True

            heading_parts = []

            if institution:
                heading_parts.append(institution)

            if period:
                heading_parts.append(period)

            if heading_parts:
                md += f"### {' | '.join(heading_parts)}\n"

            if degree:
                md += f"{degree}\n"

            if cgpa:
                md += f"CGPA: {cgpa}\n"

            md += "\n"

    if not has_education:
        md += "No education provided.\n"

    return md

# Builds the Certifications section.
def build_original_certification_markdown(certifications):

    has_cert = False
    md = "\n\n---\n\n## Certifications\n\n"

    for cert in certifications:
        cert_name = safe_text(cert.get("cert_name"))
        issuer = safe_text(cert.get("issuer"))

        # Keep using the old "year" key, but treat it as period.
        period = safe_text(
            cert.get("period")
            or cert.get("year")
        )

        if cert_name or issuer or period:
            has_cert = True

            heading_parts = []

            if cert_name:
                heading_parts.append(cert_name)

            if period:
                heading_parts.append(period)

            if heading_parts:
                md += f"### {' | '.join(heading_parts)}\n"

            if issuer:
                md += f"{issuer}\n"

            md += "\n"

    if not has_cert:
        md += "No certifications provided.\n"

    return md


# Combines all resume sections into one full Markdown resume (Header, Career Objective,Skills,Education,Work Experience,Project Experience, Certifications)
def build_full_resume_text(
    private_header,
    selected_job,
    career_objective,
    skills,
    education_md,
    experiences,
    project_list,
    cert_md,
):

    career_md = (
        "\n\n---\n\n## Career Objective\n\n"
        + safe_text(career_objective, "No career objective provided.")
        + "\n"
    )

    skills_md = (
        "\n\n---\n\n## Skills\n\n"
        + safe_text(skills, "No skills provided.")
        + "\n"
    )

    work_md = "\n\n---\n\n## Work Experience\n\n"

    has_experience = False

    if experiences:
        for exp in experiences:
            position = safe_text(exp.get("position"))
            company = safe_text(exp.get("company"))
            company_skills = safe_text(exp.get("company_skills"))
            achievement = safe_text(exp.get("achievement"))

            # Skip empty work experience form
            if not (position or company or company_skills or achievement):
                continue

            has_experience = True

            start_month = safe_text(exp.get("start_month"))
            start_year = safe_text(exp.get("start_year"))
            end_month = safe_text(exp.get("end_month"))
            end_year = safe_text(exp.get("end_year"))

            period = build_period(
                start_month=start_month,
                start_year=start_year,
                end_month=end_month,
                end_year=end_year,
            )

            bullet_points = []

            if achievement:
                bullet_points.append(achievement)

            if company_skills:
                bullet_points.append(f"Applied skills in {company_skills}.")

            work_md += build_work_experience_markdown(
                position=position,
                company=company,
                period=period,
                bullet_points=bullet_points,
            )

    if not has_experience:
        work_md += "No work experience provided.\n"

    project_md = "\n\n---\n\n## Project Experience\n\n"

    if project_list:
        has_project = False

        for project in project_list:
            project_name = safe_text(project.get("project_name"))
            project_description = safe_text(project.get("project_description"))
            project_achievement = safe_text(project.get("project_achievement"))

            if project_name or project_description or project_achievement:
                has_project = True

                project_md += f"### {project_name or 'Project Name'}\n\n"
                project_md += f"{project_description or 'No project description provided.'}\n\n"
                project_md += (
                    f"**Achievement:** "
                    f"{project_achievement or 'No project achievement provided.'}\n\n"
                )

        if not has_project:
            project_md += "No project experience provided.\n"
    else:
        project_md += "No project experience provided.\n"

    return (
        private_header
        + career_md
        + skills_md
        + education_md
        + work_md
        + project_md
        + cert_md
    )

# Checks if resume text is empty.
def confirm_text_and_start_generating_pdf(resume_text):
    if not resume_text.strip():
        st.error("Resume text is empty. Please generate or type resume content first.")
        return

    try:
        pdf_buffer = generate_resume_pdf_buffer(resume_text)

        st.success("PDF resume is ready!")

        st.download_button(
            label="⬇️ Download Resume PDF",
            data=pdf_buffer,
            file_name="resume.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    except Exception as e:
        st.error(f"PDF generation error: {e}")

# This is the main function that displays the Resume Builder page.
def render_resume_builder_page():
    section_title("📄 Resume Builder")

    if not st.session_state.get("job_recommendation_done", False):
        st.warning(
            "Please run the Job Recommendation part first and select one recommended job "
            "before using Resume Builder."
        )
        return

    selected_job = st.session_state.get("selected_job", {})
    profile = st.session_state.get("candidate_profile", {})

    if not selected_job:
        st.warning("No selected job found. Please choose a recommended job first.")
        return

    if "internship_projects" not in st.session_state:
        st.session_state["internship_projects"] = [get_default_project()]

    if "certifications" not in st.session_state:
        st.session_state["certifications"] = [get_default_certification()]

    if "editable_resume_md" not in st.session_state:
        st.session_state["editable_resume_md"] = ""

    st.markdown(f"### 🎯 Target Job - {selected_job.get('job_name', 'Selected Job')}")

    resume_type = st.radio(
        "Select Resume Type",
        ["Internship", "Permanent Worker"],
        horizontal=True,
    )

    st.divider()

    left, right = st.columns([1, 1.25], gap="large")

    with left:
        section_title("👤 Personal Information")

        full_name = st.text_input("Full Name", placeholder="Example: Rick Lopez")

        c1, c2 = st.columns([1, 1])

        with c1:
            email = st.text_input("Email", placeholder="Example: rick@email.com")

        with c2:
            phone = st.text_input("Phone Number", placeholder="Example: 0146922120")

        location = st.text_input(
            "Location",
            placeholder="Example: Kuala Lumpur, Malaysia",
        )

        use_linkedin = st.checkbox("Add LinkedIn profile")
        linkedin = ""

        if use_linkedin:
            linkedin = st.text_input("LinkedIn URL")

        use_github = st.checkbox("Add GitHub profile")
        github = ""

        if use_github:
            github = st.text_input("GitHub URL")

        profile_links = ""

        if linkedin:
            profile_links += f"LinkedIn: {linkedin}"

        if github:
            if profile_links:
                profile_links += "  \n"
            profile_links += f"GitHub: {github}"

        if not profile_links:
            profile_links = "No profile links provided"

        st.divider()

        if resume_type == "Internship":
            section_title("📌 Project Experience (Up To 4)")

            for i, project in enumerate(st.session_state["internship_projects"]):
                with st.expander(f"Project #{i + 1}", expanded=True):
                    project["project_name"] = st.text_input(
                        "Project Name",
                        value=project.get("project_name", ""),
                        placeholder = "AI-Powered Job Recommendation System",
                        key=f"project_{i}_name",
                    )

                    project["project_description"] = st.text_area(
                        "Project Description",
                        value=project.get("project_description", ""),
                        height=100,
                        placeholder = "Example : Built a Streamlit application that recommends jobs and generates tailored resumes using SBERT embeddings and a Two-Tower VAE model.",
                        key=f"project_{i}_description",
                    )

                    project["project_achievement"] = st.text_area(
                        "Project Achievement",
                        value=project.get("project_achievement", ""),
                        height=100,
                        placeholder = "Example : Developed an end-to-end AI recommendation system capable of generating personalized Top-5 to Top-10 job matches in real time.",
                        key=f"project_{i}_achievement",
                    )

                    if (
                        st.button("Remove this project", key=f"project_remove_{i}")
                        and len(st.session_state["internship_projects"]) > 1
                    ):
                        st.session_state["internship_projects"].pop(i)
                        st.rerun()

            MAX_PROJECTS = 4

            if len(st.session_state["internship_projects"]) < MAX_PROJECTS:
                if st.button("➕ Add another project"):
                    st.session_state["internship_projects"].append(get_default_project())
                    st.rerun()
            else:
                st.info(f"You can add up to {MAX_PROJECTS} projects only.")

            project_list = st.session_state["internship_projects"]

        else:
            section_title("💼 Work Experience")
            st.info("Work experience is taken from the Job Recommendation page.")
            project_list = []

        st.divider()

        section_title("🏅 Certifications (Up To 4 )")

        for i, cert in enumerate(st.session_state["certifications"]):
            with st.expander(f"Certification #{i + 1}", expanded=True):
                cert["cert_name"] = st.text_input(
                    "Certification Name",
                    value=cert.get("cert_name", ""),
                    placeholder = "Example : Amazon Database Course",
                    key=f"cert_{i}_name",
                )

                cert["issuer"] = st.text_input(
                    "Issuer / Organization",
                    value=cert.get("issuer", ""),
                    placeholder = "Example : Google",
                    key=f"cert_{i}_issuer",
                )

                cert["year"] = st.text_input(
                    "Period",
                    value=cert.get("year", ""),
                    placeholder="Example: Jan 2024 - Mar 2024",
                    key=f"cert_{i}_year",
                )

                if (
                    st.button("Remove this certification", key=f"cert_remove_{i}")
                    and len(st.session_state["certifications"]) > 1
                ):
                    st.session_state["certifications"].pop(i)
                    st.rerun()

        MAX_CERTIFICATIONS = 4

        if len(st.session_state["certifications"]) < MAX_CERTIFICATIONS:
            if st.button("➕ Add another certification"):
                st.session_state["certifications"].append(get_default_certification())
                st.rerun()
        else:
            st.info(f"You can add up to {MAX_CERTIFICATIONS} certifications only.")

    with right:
        section_title("📄 Resume Text Box")

        career_objective = safe_text(profile.get("career_objective"))
        skills = safe_text(profile.get("skills"))
        education_list = profile.get("education_details", [])
        experiences = profile.get("experiences", [])

        private_header = build_private_header(
            full_name=full_name,
            email=email,
            phone=phone,
            location=location,
            profile_links=profile_links,
        )

        clean_experiences = [
            exp for exp in experiences
            if exp.get("position") or exp.get("company") or exp.get("company_skills") or exp.get("achievement")
        ]
        llm_resume_input = {
            "resume_type": resume_type,
            "career_objective": career_objective,
            "skills": skills,
            "experiences": clean_experiences,
            "projects": project_list,
            "selected_job": {
                "job_name": selected_job.get("job_name", ""),
                "job_text": selected_job.get("job_text", ""),
            },
        }

        education_md = build_original_education_markdown(education_list)
        cert_md = build_original_certification_markdown(
            st.session_state["certifications"]
        )

        # Add this block here
        if not st.session_state["editable_resume_md"]:
            st.session_state["editable_resume_md"] = build_full_resume_text(
                private_header=private_header,
                selected_job=selected_job,
                career_objective=career_objective,
                skills=skills,
                education_md=education_md,
                experiences=experiences,
                project_list=project_list,
                cert_md=cert_md,
            )

        refresh_button, ollama_button = st.columns([1, 1])

        with refresh_button:
            if st.button(
                "🔄 Refresh Resume Text",
                use_container_width=True,
            ):
                st.session_state["editable_resume_md"] = build_full_resume_text(
                    private_header=private_header,
                    selected_job=selected_job,
                    career_objective=career_objective,
                    skills=skills,
                    education_md=education_md,
                    experiences=experiences,
                    project_list=project_list,
                    cert_md=cert_md,
                )

        with ollama_button:
            if st.button(
                "Generate Resume with Ollama",
                type="primary",
                use_container_width=True,
            ):
                with st.spinner("Generating resume using Ollama..."):
                    ai_modified_sections = generate_resume_with_ollama(
                        PROMPT_PATH,
                        llm_resume_input,
                    )

                    if ai_modified_sections:
                        st.session_state["editable_resume_md"] = (
                            private_header
                            + "\n\n"
                            + ai_modified_sections
                            + education_md
                            + cert_md
                        )

        st.text_area(
            "Resume Content",
            key="editable_resume_md",
            height=750,
        )

        st.divider()

        if st.button(
            "✅ Confirm Text and Start Generating PDF",
            type="primary",
            use_container_width=True,
        ):
            confirm_text_and_start_generating_pdf(
                st.session_state["editable_resume_md"]
            )
