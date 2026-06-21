import io

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth


PAGE_WIDTH, PAGE_HEIGHT = A4

LEFT_MARGIN = 45
RIGHT_MARGIN = 45
TOP_MARGIN = 35
BOTTOM_MARGIN = 35

CONTENT_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN

FIXED_SCALE = 1.3


# Function to remove markdown symbols before drawing text into PDF.
def clean_md(text):
    text = str(text)
    text = text.replace("**", "")
    text = text.replace("### ", "")
    text = text.replace("## ", "")
    text = text.replace("# ", "")
    return text.strip()


# Creates fixed font sizes and spacing values.
def get_layout_settings(scale=FIXED_SCALE, extra_gap=0):
    return {
        "scale": scale,

        "name_font": 24 * scale,
        "contact_font": 8.5 * scale,

        "section_font": 12 * scale,
        "subheading_font": 9.3 * scale,
        "body_font": 8.8 * scale,
        "bullet_font": 8.6 * scale,
        "skill_font": 8.8 * scale,

        "name_gap": 22 * scale,
        "contact_gap": 15 * scale,

        "section_line_gap": 6 * scale,
        "content_after_line_gap": 12 * scale,
        "section_bottom_gap": 18 * scale,

        "body_leading": 11.5 * scale,
        "about_leading": 13 * scale,
        "bullet_leading": 11 * scale,
        "small_gap": 4 * scale,
        "entry_gap": 7 * scale,
    }


# Extract the name from the text box.
def get_resume_name(resume_text):
    for line in resume_text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return clean_md(line)
    return "YOUR NAME"


# Splits the resume text into sections.
def split_resume_sections(resume_text):
    sections = {"HEADER": []}
    current_section = "HEADER"

    for line in resume_text.splitlines():
        line = line.rstrip()

        if line.strip() == "---":
            continue

        if line.startswith("## "):
            current_section = clean_md(line).upper()
            if current_section not in sections:
                sections[current_section] = []
        else:
            sections.setdefault(current_section, []).append(line)

    return sections


# Reads the header section and extracts phone, email, location and profile links.
def extract_contact_items(header_lines):
    contact = {
        "phone": "",
        "email": "",
        "location": "",
        "profile": "",
    }

    profile_parts = []

    for line in header_lines:
        text = clean_md(line)

        if not text:
            continue

        lower_text = text.lower()

        if lower_text.startswith("phone:"):
            contact["phone"] = text.split(":", 1)[1].strip()

        elif lower_text.startswith("email:"):
            contact["email"] = text.split(":", 1)[1].strip()

        elif lower_text.startswith("location:"):
            contact["location"] = text.split(":", 1)[1].strip()

        elif lower_text.startswith("profile links:"):
            continue

        elif "no profile links" in lower_text:
            continue

        elif (
            "linkedin" in lower_text
            or "github" in lower_text
            or "portfolio" in lower_text
        ):
            profile_parts.append(text)

    contact["profile"] = " | ".join(profile_parts)
    return contact


# Breaks long text into multiple lines so it does not go outside the PDF margin.
def wrap_text(text, font_name, font_size, max_width):
    text = clean_md(text)

    if not text:
        return []

    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = word if not current_line else current_line + " " + word

        if stringWidth(test_line, font_name, font_size) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines
    
def draw_justified_line(c, line, x, y, max_width, font_name, font_size):
    words = line.split()

    # Do not justify short lines or single-word lines.
    if len(words) <= 1:
        c.drawString(x, y, line)
        return

    words_width = sum(stringWidth(word, font_name, font_size) for word in words)
    space_count = len(words) - 1
    extra_space = (max_width - words_width) / space_count

    current_x = x

    for word in words:
        c.drawString(current_x, y, word)
        current_x += stringWidth(word, font_name, font_size) + extra_space

# Creates a new page and returns the starting y position.
def start_new_page(c):
    c.showPage()
    c.setFillColor(colors.black)
    return PAGE_HEIGHT - TOP_MARGIN


# Checks if enough vertical space remains; if not, continue on a new page.
def ensure_space(c, y, required_height):
    if y - required_height < BOTTOM_MARGIN:
        return start_new_page(c)
    return y


# Draws a grey horizontal line.
def draw_horizontal_line(c, y):
    c.setStrokeColor(colors.grey)
    c.setLineWidth(0.8)
    c.line(LEFT_MARGIN, y, PAGE_WIDTH - RIGHT_MARGIN, y)
    c.setStrokeColor(colors.black)


# Draws one wrapped text block and automatically continues on a new page if needed.
def draw_wrapped_text(c,text,x,y,max_width,font_name,font_size,leading,justify=True,):
    lines = wrap_text(text, font_name, font_size, max_width)

    c.setFont(font_name, font_size)

    for index, line in enumerate(lines):
        y = ensure_space(c, y, leading)
        c.setFont(font_name, font_size)

        is_last_line = index == len(lines) - 1

        # Justify all lines except the last line.
        if justify and not is_last_line:
            draw_justified_line(
                c=c,
                line=line,
                x=x,
                y=y,
                max_width=max_width,
                font_name=font_name,
                font_size=font_size,
            )
        else:
            c.drawString(x, y, line)

        y -= leading

    return y

# Draws the top header of the resume.
def draw_header(c, resume_name, contact, settings, y):
    name_font = settings["name_font"]
    contact_font = settings["contact_font"]

    name = clean_md(resume_name).upper()

    c.setFont("Helvetica-Bold", name_font)
    name_width = stringWidth(name, "Helvetica-Bold", name_font)
    c.drawString((PAGE_WIDTH - name_width) / 2, y, name)

    y -= settings["name_gap"]

    contact_items = []

    if contact.get("phone"):
        contact_items.append("Phone: " + contact["phone"])

    if contact.get("email"):
        contact_items.append("Email: " + contact["email"])

    if contact.get("location"):
        contact_items.append("Location: " + contact["location"])

    if not contact_items:
        contact_items = ["Phone:", "Email:", "Location:"]

    contact_text = clean_md(" | ".join(contact_items))

    while (
        stringWidth(contact_text, "Helvetica", contact_font) > CONTENT_WIDTH
        and len(contact_text) > 6
    ):
        contact_text = contact_text[:-4] + "..."

    c.setFont("Helvetica", contact_font)
    contact_width = stringWidth(contact_text, "Helvetica", contact_font)
    contact_x = (PAGE_WIDTH - contact_width) / 2
    c.drawString(contact_x, y, contact_text)

    y -= settings["contact_gap"]

    if contact.get("profile"):
        profile_lines = wrap_text(
            text=contact["profile"],
            font_name="Helvetica",
            font_size=contact_font,
            max_width=CONTENT_WIDTH,
        )

        c.setFont("Helvetica", contact_font)

        for profile_line in profile_lines:
            line_width = stringWidth(profile_line, "Helvetica", contact_font)
            profile_x = (PAGE_WIDTH - line_width) / 2
            c.drawString(profile_x, y, profile_line)
            y -= settings["body_leading"]

        y -= settings["small_gap"]

    return y - settings["section_bottom_gap"]


# Draws section title, then a horizontal line, then returns y for content.
def draw_section_header(c, title, y, settings):
    required_height = (
        settings["section_font"]
        + settings["section_line_gap"]
        + settings["content_after_line_gap"]
        + settings["body_leading"]
    )

    y = ensure_space(c, y, required_height)

    c.setFont("Helvetica-Bold", settings["section_font"])
    c.setFillColor(colors.black)
    c.drawString(LEFT_MARGIN, y, title.upper())

    line_y = y - settings["section_line_gap"]
    draw_horizontal_line(c, line_y)

    return line_y - settings["content_after_line_gap"]


# Draws normal markdown lines inside a section.
def draw_general_markdown_lines(c, lines, y, max_width, settings):
    previous_was_entry = False

    for line in lines:
        original_line = line.strip()

        if not original_line:
            continue

        # Add extra space before every new project / work experience item
        # because each item starts with ###.
        if original_line.startswith("### "):
            if previous_was_entry:
                y -= settings["entry_gap"]

            y = ensure_space(c, y, settings["body_leading"])
            text = clean_md(original_line)
            c.setFont("Helvetica-Bold", settings["subheading_font"])
            c.drawString(LEFT_MARGIN, y, text)
            y -= settings["body_leading"]

            previous_was_entry = True

        elif original_line.startswith("- "):
            bullet_text = clean_md(original_line.replace("- ", "", 1))
            bullet_x = LEFT_MARGIN + 20
            bullet_width = max_width - 22

            wrapped = wrap_text(
                bullet_text,
                "Helvetica",
                settings["bullet_font"],
                bullet_width,
            )

            c.setFont("Helvetica", settings["bullet_font"])

            for index, wrapped_line in enumerate(wrapped):
                y = ensure_space(c, y, settings["bullet_leading"])
                c.setFont("Helvetica", settings["bullet_font"])

                is_first_line = index == 0
                is_last_line = index == len(wrapped) - 1

                if is_first_line:
                    c.drawString(LEFT_MARGIN + 8, y, u"\u2022")

                # Justify bullet continuation text except the last line.
                if not is_last_line:
                    draw_justified_line(
                        c=c,
                        line=wrapped_line,
                        x=bullet_x,
                        y=y,
                        max_width=bullet_width,
                        font_name="Helvetica",
                        font_size=settings["bullet_font"],
                    )
                else:
                    c.drawString(bullet_x, y, wrapped_line)

                y -= settings["bullet_leading"]

            previous_was_entry = False

        else:
            font_name = "Helvetica-Bold" if original_line.startswith("**") else "Helvetica"

            y = draw_wrapped_text(
                c=c,
                text=original_line,
                x=LEFT_MARGIN,
                y=y,
                max_width=max_width,
                font_name=font_name,
                font_size=settings["body_font"],
                leading=settings["body_leading"],
                justify=True,
            )

            previous_was_entry = False

    return y


# Draws one complete section in this structure:
# SECTION TITLE
# horizontal line
# content
# fixed section gap
# next section
def draw_text_section(c, title, lines, y, settings):
    clean_lines = [line for line in lines if line.strip()]

    if not clean_lines:
        return y

    y = draw_section_header(c, title, y, settings)

    y = draw_general_markdown_lines(
        c=c,
        lines=clean_lines,
        y=y,
        max_width=CONTENT_WIDTH,
        settings=settings,
    )

    return y - settings["section_bottom_gap"]


# Draws a paragraph-style section such as Professional Summary / Career Objective.
def draw_paragraph_section(c, title, lines, y, settings):
    clean_lines = [clean_md(line) for line in lines if line.strip()]

    if not clean_lines:
        return y

    y = draw_section_header(c, title, y, settings)

    paragraph = " ".join(clean_lines)

    y = draw_wrapped_text(
        c=c,
        text=paragraph,
        x=LEFT_MARGIN,
        y=y,
        max_width=CONTENT_WIDTH,
        font_name="Helvetica",
        font_size=settings["body_font"],
        leading=settings["about_leading"],
    )

    return y - settings["section_bottom_gap"]


# Normalizes skills so both bullet skills and comma-separated skills can be shown.
def normalize_skill_text(lines):
    skill_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        text = clean_md(line)

        # If already formatted like:
        # Technical Skills: Python, SQL, Excel
        if ":" in text:
            skill_lines.append(text)
            continue

        # If old bullet format still appears, remove the dash
        if line.startswith("- "):
            text = clean_md(line.replace("- ", "", 1))

        if text:
            skill_lines.append(text)

    return skill_lines


# Draws skills using the same fixed section structure.
def draw_skills(c, lines, y, settings):
    skill_lines = normalize_skill_text(lines)

    if not skill_lines:
        return y

    y = draw_section_header(c, "SKILLS", y, settings)

    for skill_line in skill_lines:
        y = draw_wrapped_text(
            c=c,
            text=skill_line,
            x=LEFT_MARGIN,
            y=y,
            max_width=CONTENT_WIDTH,
            font_name="Helvetica",
            font_size=settings["skill_font"],
            leading=settings["body_leading"],
            justify=False,
        )

    return y - settings["section_bottom_gap"]

# This is the main function called by the resume builder.
def render_resume_layout(c, resume_text, scale=FIXED_SCALE, extra_gap=0):
    settings = get_layout_settings(scale, extra_gap)

    sections = split_resume_sections(resume_text)

    resume_name = get_resume_name(resume_text)
    contact = extract_contact_items(sections.get("HEADER", []))

    y = PAGE_HEIGHT - TOP_MARGIN

    y = draw_header(
        c=c,
        resume_name=resume_name,
        contact=contact,
        settings=settings,
        y=y,
    )

    # Support both AI-generated and original resume headings.
    if any(line.strip() for line in sections.get("PROFESSIONAL SUMMARY", [])):
        y = draw_paragraph_section(
            c=c,
            title="PROFESSIONAL SUMMARY",
            lines=sections.get("PROFESSIONAL SUMMARY", []),
            y=y,
            settings=settings,
        )
    elif any(line.strip() for line in sections.get("CAREER OBJECTIVE", [])):
        y = draw_paragraph_section(
            c=c,
            title="CAREER OBJECTIVE",
            lines=sections.get("CAREER OBJECTIVE", []),
            y=y,
            settings=settings,
        )

    y = draw_text_section(
        c=c,
        title="EDUCATION",
        lines=sections.get("EDUCATION", []),
        y=y,
        settings=settings,
    )

    y = draw_text_section(
        c=c,
        title="WORK EXPERIENCE",
        lines=sections.get("WORK EXPERIENCE", []),
        y=y,
        settings=settings,
    )

    y = draw_text_section(
        c=c,
        title="PROJECT EXPERIENCE",
        lines=sections.get("PROJECT EXPERIENCE", []),
        y=y,
        settings=settings,
    )

    y = draw_skills(
        c=c,
        lines=sections.get("SKILLS", []),
        y=y,
        settings=settings,
    )

    y = draw_text_section(
        c=c,
        title="CERTIFICATIONS",
        lines=sections.get("CERTIFICATIONS", []),
        y=y,
        settings=settings,
    )

    return y


def generate_resume_pdf_buffer(resume_text):
    if not resume_text.strip():
        raise ValueError("Resume text is empty.")

    pdf_buffer = io.BytesIO()

    c = canvas.Canvas(pdf_buffer, pagesize=A4)

    render_resume_layout(
        c=c,
        resume_text=resume_text,
        scale=FIXED_SCALE,
        extra_gap=0,
    )

    c.save()

    pdf_buffer.seek(0)
    return pdf_buffer
