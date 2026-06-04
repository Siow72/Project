import io
import re

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

MIN_SCALE = 0.78
MAX_SCALE = 1.16

# functi9on to remove markdown symbols "#"
def clean_md(text):
    text = str(text)
    text = text.replace("**", "")
    text = text.replace("### ", "")
    text = text.replace("## ", "")
    text = text.replace("# ", "")
    return text.strip()

# Creates all font sizes and spacing values based on the selected scale.
def get_layout_settings(scale, extra_gap=0):
    return {
        "scale": scale,
        "extra_gap": extra_gap,

        "name_font": 24 * scale,
        "contact_font": 8.5 * scale,

        "section_font": 12 * scale,
        "subheading_font": 9.3 * scale,
        "body_font": 8.8 * scale,
        "bullet_font": 8.6 * scale,
        "skill_font": 8.8 * scale,

        "name_gap": 22 * scale,
        "contact_gap": 15 * scale,

        "section_title_gap": 20 * scale,
        "section_bottom_gap": (14 * scale) + extra_gap,
        "line_after_section_gap": (18 * scale) + extra_gap,

        "body_leading": 11.5 * scale,
        "about_leading": 13 * scale,
        "bullet_leading": 11 * scale,
        "skill_row_height": 13 * scale,

        "small_gap": 4 * scale,
    }

# Extract the name from the text box
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
            sections[current_section] = []
        else:
            sections[current_section].append(line)

    return sections

# Reads the header section and extracts :phone,email, location, profile links
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

# Draws wrapped text onto the PDF line by line.
def draw_wrapped_text(
    c,
    text,
    x,
    y,
    max_width,
    font_name,
    font_size,
    leading,
    draw=True,
):
    lines = wrap_text(text, font_name, font_size, max_width)

    if draw and c:
        c.setFont(font_name, font_size)

    for line in lines:
        if draw and c:
            c.drawString(x, y, line)
        y -= leading

    return y

# Draws a grey horizontal line between resume sections.
def draw_horizontal_line(c, y, draw=True):
    if draw and c:
        c.setStrokeColor(colors.grey)
        c.setLineWidth(0.8)
        c.line(LEFT_MARGIN, y, PAGE_WIDTH - RIGHT_MARGIN, y)

# Draws the top part of the resume
def draw_header(c, resume_name, contact, settings, y, draw=True):
    name_font = settings["name_font"]
    contact_font = settings["contact_font"]

    # Name
    name = clean_md(resume_name).upper()

    if draw and c:
        c.setFont("Helvetica-Bold", name_font)
        name_width = stringWidth(name, "Helvetica-Bold", name_font)
        c.drawString((PAGE_WIDTH - name_width) / 2, y, name)

    y -= settings["name_gap"]

    # First contact row: Phone, Email, Location, centered
    contact_items = []

    if contact.get("phone"):
        contact_items.append("Phone: " + contact["phone"])

    if contact.get("email"):
        contact_items.append("Email: " + contact["email"])

    if contact.get("location"):
        contact_items.append("Location: " + contact["location"])

    if not contact_items:
        contact_items = ["Phone:", "Email:", "Location:"]

    contact_text = " | ".join(contact_items)
    contact_text = clean_md(contact_text)

    if draw and c:
        c.setFont("Helvetica", contact_font)

    # Shorten if too long
    while (
        stringWidth(contact_text, "Helvetica", contact_font) > CONTENT_WIDTH
        and len(contact_text) > 6
    ):
        contact_text = contact_text[:-4] + "..."

    if draw and c:
        contact_width = stringWidth(contact_text, "Helvetica", contact_font)
        contact_x = (PAGE_WIDTH - contact_width) / 2
        c.drawString(contact_x, y, contact_text)

    y -= settings["contact_gap"]

    # Second contact row: LinkedIn / GitHub / Portfolio, centered
    if contact.get("profile"):
        profile_text = clean_md(contact["profile"])

        if draw and c:
            c.setFont("Helvetica", contact_font)

        wrapped_profile_lines = wrap_text(
            text=profile_text,
            font_name="Helvetica",
            font_size=contact_font,
            max_width=CONTENT_WIDTH,
        )

        for profile_line in wrapped_profile_lines:
            if draw and c:
                line_width = stringWidth(profile_line, "Helvetica", contact_font)
                profile_x = (PAGE_WIDTH - line_width) / 2
                c.drawString(profile_x, y, profile_line)

            y -= settings["body_leading"]

        y -= settings["small_gap"]

    draw_horizontal_line(c, y, draw=draw)

    return y - settings["line_after_section_gap"]

# Draws section titles 
def draw_section_title(c, title, y, settings, draw=True):
    if draw and c:
        c.setFont("Helvetica-Bold", settings["section_font"])
        c.setFillColor(colors.black)
        c.drawString(LEFT_MARGIN, y, title.upper())

    return y - settings["section_title_gap"]

# Draws normal resume lines.
def draw_general_markdown_lines(c, lines, y, max_width, settings, draw=True):

    for line in lines:
        line = line.strip()

        if not line:
            y -= settings["small_gap"]
            continue

        if line.startswith("### "):
            text = clean_md(line)

            if draw and c:
                c.setFont("Helvetica-Bold", settings["subheading_font"])
                c.drawString(LEFT_MARGIN, y, text)

            y -= settings["body_leading"]

        elif line.startswith("- "):
            bullet_text = clean_md(line.replace("- ", "", 1))
            wrapped = wrap_text(
                bullet_text,
                "Helvetica",
                settings["bullet_font"],
                max_width - 22,
            )

            if draw and c:
                c.setFont("Helvetica", settings["bullet_font"])

            first_line = True

            for wrapped_line in wrapped:
                if draw and c:
                    if first_line:
                        c.drawString(LEFT_MARGIN + 8, y, u"\u2022")
                        c.drawString(LEFT_MARGIN + 20, y, wrapped_line)
                    else:
                        c.drawString(LEFT_MARGIN + 20, y, wrapped_line)

                first_line = False
                y -= settings["bullet_leading"]

        else:
            font_name = "Helvetica-Bold" if line.startswith("**") else "Helvetica"

            y = draw_wrapped_text(
                c=c,
                text=clean_md(line),
                x=LEFT_MARGIN,
                y=y,
                max_width=max_width,
                font_name=font_name,
                font_size=settings["body_font"],
                leading=settings["body_leading"],
                draw=draw,
            )

    return y

# Draws a full normal section
def draw_text_section(c, title, lines, y, settings, draw=True):
    clean_lines = [line for line in lines if line.strip()]

    if not clean_lines:
        return y

    y = draw_section_title(c, title, y, settings, draw=draw)

    y = draw_general_markdown_lines(
        c=c,
        lines=clean_lines,
        y=y,
        max_width=CONTENT_WIDTH,
        settings=settings,
        draw=draw,
    )

    y -= settings["section_bottom_gap"]
    draw_horizontal_line(c, y, draw=draw)

    return y - settings["line_after_section_gap"]


def split_certification_blocks(lines):
    blocks = []
    current_block = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("### "):
            if current_block:
                blocks.append(current_block)

            current_block = [line]
        else:
            if current_block:
                current_block.append(line)
            else:
                current_block = [line]

    if current_block:
        blocks.append(current_block)

    return blocks


def measure_certification_block(block, column_width, settings):
    total_height = 0

    for line in block:
        line = line.strip()

        if not line:
            continue

        if line.startswith("### "):
            font_name = "Helvetica-Bold"
            font_size = settings["subheading_font"]
        else:
            font_name = "Helvetica-Bold" if line.startswith("**") else "Helvetica"
            font_size = settings["body_font"]

        wrapped_lines = wrap_text(
            text=clean_md(line),
            font_name=font_name,
            font_size=font_size,
            max_width=column_width,
        )

        line_count = max(1, len(wrapped_lines))
        total_height += line_count * settings["body_leading"]

    return total_height


def draw_certification_block(c, block, x, y, column_width, settings, draw=True):
    for line in block:
        line = line.strip()

        if not line:
            continue

        if line.startswith("### "):
            font_name = "Helvetica-Bold"
            font_size = settings["subheading_font"]
        else:
            font_name = "Helvetica-Bold" if line.startswith("**") else "Helvetica"
            font_size = settings["body_font"]

        wrapped_lines = wrap_text(
            text=clean_md(line),
            font_name=font_name,
            font_size=font_size,
            max_width=column_width,
        )

        if draw and c:
            c.setFont(font_name, font_size)

        for wrapped_line in wrapped_lines:
            if draw and c:
                c.drawString(x, y, wrapped_line)

            y -= settings["body_leading"]

    return y

# They organize certifications into two columns to save space.
def draw_certifications(c, lines, y, settings, draw=True):
    clean_lines = [line for line in lines if line.strip()]

    if not clean_lines:
        return y

    blocks = split_certification_blocks(clean_lines)

    if not blocks:
        return y

    y = draw_section_title(c, "CERTIFICATIONS", y, settings, draw=draw)

    column_gap = 25 * settings["scale"]
    column_width = (CONTENT_WIDTH - column_gap) / 2

    left_x = LEFT_MARGIN
    right_x = LEFT_MARGIN + column_width + column_gap

    row_gap = settings["small_gap"] * 2

    index = 0

    while index < len(blocks):
        left_block = blocks[index]
        right_block = blocks[index + 1] if index + 1 < len(blocks) else None

        row_start_y = y

        left_height = measure_certification_block(
            block=left_block,
            column_width=column_width,
            settings=settings,
        )

        right_height = 0

        if right_block:
            right_height = measure_certification_block(
                block=right_block,
                column_width=column_width,
                settings=settings,
            )

        draw_certification_block(
            c=c,
            block=left_block,
            x=left_x,
            y=row_start_y,
            column_width=column_width,
            settings=settings,
            draw=draw,
        )

        if right_block:
            draw_certification_block(
                c=c,
                block=right_block,
                x=right_x,
                y=row_start_y,
                column_width=column_width,
                settings=settings,
                draw=draw,
            )

        row_height = max(left_height, right_height)
        y = row_start_y - row_height - row_gap

        index += 2

    y -= settings["section_bottom_gap"]
    draw_horizontal_line(c, y, draw=draw)

    return y - settings["line_after_section_gap"]

# Draws the Professional Summary section, but labels it as About Me
def draw_about_me(c, lines, y, settings, draw=True):
    clean_lines = [clean_md(line) for line in lines if line.strip()]

    if not clean_lines:
        return y

    y = draw_section_title(c, "ABOUT ME", y, settings, draw=draw)

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
        draw=draw,
    )

    y -= settings["section_bottom_gap"]
    draw_horizontal_line(c, y, draw=draw)

    return y - settings["line_after_section_gap"]

# Draws skills in three columns.
def draw_skills(c, lines, y, settings, draw=True):
    skills = []

    for line in lines:
        line = line.strip()

        if line.startswith("- "):
            skill = clean_md(line.replace("- ", "", 1))
            if skill:
                skills.append(skill)

    if not skills:
        return y

    y = draw_section_title(c, "SKILLS", y, settings, draw=draw)

    columns = 3
    column_width = CONTENT_WIDTH / columns
    row_height = settings["skill_row_height"]

    if draw and c:
        c.setFont("Helvetica", settings["skill_font"])

    for index, skill in enumerate(skills):
        col = index % columns
        row = index // columns

        x = LEFT_MARGIN + col * column_width
        skill_y = y - row * row_height

        if draw and c:
            c.drawString(x, skill_y, u"\u2022")
            c.drawString(x + 12, skill_y, skill)

    rows = (len(skills) + columns - 1) // columns
    y -= rows * row_height

    y -= settings["section_bottom_gap"]
    draw_horizontal_line(c, y, draw=draw)

    return y - settings["line_after_section_gap"]

#Counts how many resume sections contain content.
def count_non_empty_sections(sections):
    section_names = [
        "PROFESSIONAL SUMMARY",
        "EDUCATION",
        "WORK EXPERIENCE",
        "PROJECT EXPERIENCE",
        "SKILLS",
        "CERTIFICATIONS",
    ]

    count = 0

    for section_name in section_names:
        lines = sections.get(section_name, [])
        if any(line.strip() for line in lines):
            count += 1

    return max(count, 1)

#This is the main function called by the resume builder.
'''
Checks resume text is not empty.
Chooses the best layout size.
Creates a PDF in memory.
Draws the resume.
Adds a warning if the content is too long.
Returns the PDF buffer for download.
'''
def render_resume_layout(
    c,
    resume_text,
    scale,
    extra_gap=0,
    draw=True,
):
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
        draw=draw,
    )

    y = draw_about_me(
        c=c,
        lines=sections.get("PROFESSIONAL SUMMARY", []),
        y=y,
        settings=settings,
        draw=draw,
    )

    y = draw_text_section(
        c=c,
        title="EDUCATION",
        lines=sections.get("EDUCATION", []),
        y=y,
        settings=settings,
        draw=draw,
    )

    y = draw_text_section(
        c=c,
        title="WORK EXPERIENCE",
        lines=sections.get("WORK EXPERIENCE", []),
        y=y,
        settings=settings,
        draw=draw,
    )

    y = draw_text_section(
        c=c,
        title="PROJECT EXPERIENCE",
        lines=sections.get("PROJECT EXPERIENCE", []),
        y=y,
        settings=settings,
        draw=draw,
    )

    y = draw_skills(
        c=c,
        lines=sections.get("SKILLS", []),
        y=y,
        settings=settings,
        draw=draw,
    )

    y = draw_certifications(
        c=c,
        lines=sections.get("CERTIFICATIONS", []),
        y=y,
        settings=settings,
        draw=draw,
    )

    return y

# Automatically chooses the best font scale.
def choose_auto_layout(resume_text):
    low = MIN_SCALE
    high = MAX_SCALE

    # If it cannot fit even at minimum scale, use minimum scale.
    min_final_y = render_resume_layout(
        c=None,
        resume_text=resume_text,
        scale=MIN_SCALE,
        extra_gap=0,
        draw=False,
    )

    if min_final_y < BOTTOM_MARGIN:
        return MIN_SCALE, 0, False

    # Binary search for biggest fitting scale.
    for _ in range(22):
        mid = (low + high) / 2

        final_y = render_resume_layout(
            c=None,
            resume_text=resume_text,
            scale=mid,
            extra_gap=0,
            draw=False,
        )

        if final_y >= BOTTOM_MARGIN:
            low = mid
        else:
            high = mid

    best_scale = low

    # Add extra spacing if there is still too much empty space.
    sections = split_resume_sections(resume_text)
    section_count = count_non_empty_sections(sections)

    final_y = render_resume_layout(
        c=None,
        resume_text=resume_text,
        scale=best_scale,
        extra_gap=0,
        draw=False,
    )

    empty_space = max(0, final_y - BOTTOM_MARGIN)

    # Do not add too much gap, otherwise it looks strange.
    extra_gap = min(empty_space / section_count * 0.45, 10)

    return best_scale, extra_gap, True


def generate_resume_pdf_buffer(resume_text):
    if not resume_text.strip():
        raise ValueError("Resume text is empty.")

    scale, extra_gap, fits_one_page = choose_auto_layout(
        resume_text=resume_text,
    )

    pdf_buffer = io.BytesIO()

    c = canvas.Canvas(pdf_buffer, pagesize=A4)

    final_y = render_resume_layout(
        c=c,
        resume_text=resume_text,
        scale=scale,
        extra_gap=extra_gap,
        draw=True,
    )

    # If content still overflows at minimum scale, add note instead of clipping silently.
    if final_y < BOTTOM_MARGIN:
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.red)
        c.drawString(
            LEFT_MARGIN,
            18,
            "Note: Resume content is too long for one A4 page. Please shorten the text for best formatting.",
        )
        c.setFillColor(colors.black)

    c.save()

    pdf_buffer.seek(0)
    return pdf_buffer