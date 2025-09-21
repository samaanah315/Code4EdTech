import re
import os
import spacy
from parse_files import extract_pdf_text, extract_docx_text

# Load small English NLP model
nlp = spacy.load("en_core_web_sm")

# ------------------ Functions ------------------

def get_jd_text(jd_file):
    """Extract text from JD file (PDF, DOCX, or TXT)."""
    if jd_file.lower().endswith(".pdf"):
        return extract_pdf_text(jd_file)
    elif jd_file.lower().endswith(".docx"):
        return extract_docx_text(jd_file)
    elif jd_file.lower().endswith(".txt"):
        with open(jd_file, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return ""

def split_roles(jd_text):
    """Split JD text into sections based on numbering or bullets."""
    sections = re.split(r"\n\d+\.\s", jd_text)  # e.g., "1. Role"
    return [sec.strip() for sec in sections if sec.strip()]

def get_role_title(section_text):
    """Get role title: usually first non-empty line"""
    lines = section_text.split("\n")
    for line in lines:
        if line.strip():
            return line.strip()
    return "Unknown Role"

def get_skills(section_text):
    """Extract skills from the section"""
    skills = []
    # Look for "Skills:" section
    skills_match = re.search(r"Skills:([\s\S]+?)(?:Eligibility|$)", section_text, re.IGNORECASE)
    if skills_match:
        skills = [s.strip() for s in skills_match.group(1).split(",")]

    # Fallback: bullets containing known tech keywords
    keywords = ["Python", "R", "SQL", "Spark", "Pandas", "Machine Learning", "Deep Learning",
                "NLP", "Excel", "Tableau", "Power BI", "Docker", "Git"]
    for line in section_text.split("\n"):
        if line.startswith("•") and any(k.lower() in line.lower() for k in keywords):
            skills.append(line.strip("• ").strip())
    return list(set(skills))  # remove duplicates

def get_qualifications(section_text):
    """Extract degrees/qualifications"""
    qual_pattern = r"(B\.Tech|BE|Bachelor's|Master's|PhD)"
    return re.findall(qual_pattern, section_text, re.IGNORECASE)

def parse_jd_file(jd_file):
    """Parse a JD file and return list of roles with role_title, skills, qualifications, and text"""
    jd_text = get_jd_text(jd_file)
    sections = split_roles(jd_text)
    parsed_roles = []

    # If no sections found, treat whole JD as single section
    if not sections:
        sections = [jd_text]

    for sec in sections:
        parsed_roles.append({
            "role_title": get_role_title(sec),
            "skills": get_skills(sec),
            "qualifications": get_qualifications(sec),
            "text": sec
        })
    return parsed_roles

def parse_all_jds(folder="JDS"):
    """Parse all JD files in a folder and return a dictionary: {filename: parsed_roles}"""
    all_jds = {}
    if not os.path.exists(folder):
        print(f"Folder '{folder}' does not exist!")
        return all_jds

    files = [f for f in os.listdir(folder) if f.lower().endswith((".txt", ".pdf", ".docx"))]
    for f in files:
        path = os.path.join(folder, f)
        all_jds[f] = parse_jd_file(path)
    return all_jds

# ------------------ Quick Test ------------------
if __name__ == "__main__":
    parsed_jds = parse_all_jds("JDS")
    for filename, roles in parsed_jds.items():
        print(f"====== {filename} ======")
        for i, role in enumerate(roles, 1):
            print(f"--- Role {i} ---")
            print("Role Title:", role["role_title"])
            print("Skills:", role["skills"])
            print("Qualifications:", role["qualifications"])
            print("Text snippet:", role["text"][:200])
            print("\n")
