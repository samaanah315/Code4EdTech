# skill_extraction.py
import re

def extract_skills_from_resume(resume_file):
    """Extract skills from a resume (plain text)"""
    skills = []
    with open(resume_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    capture = False
    for line in lines:
        line = line.strip()
        if re.search(r"(skills|technologies|tools)", line, re.I):
            capture = True
            skills.extend([x.strip() for x in re.split(r",|;", line)])
        elif capture:
            if line.startswith("•") or line:
                skills.extend([x.strip() for x in re.split(r",|;", line)])
            else:
                break
    return [s for s in skills if s]

def extract_projects_and_certifications(resume_file):
    """Extract projects and certifications from resumes"""
    projects = []
    certifications = []
    with open(resume_file, "r", encoding="utf-8") as f:
        text = f.read()
    # Simple regex for projects (keywords like 'project', 'analysis', etc.)
    project_matches = re.findall(r"(.*project.*|.*analysis.*|.*dashboard.*|.*data.*:.*)", text, re.I)
    projects.extend(project_matches)
    # Simple regex for certifications
    cert_matches = re.findall(r"(certified.*|certification.*|– [^\n]+)", text, re.I)
    certifications.extend(cert_matches)
    return projects, certifications

def extract_skills_from_jd(jd_file):
    """Extract must-have and good-to-have skills from JD"""
    skills = []
    good_to_have = []
    with open(jd_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    capture_skills = False
    capture_good = False
    for line in lines:
        line = line.strip()
        if line.startswith("• Skills:"):
            capture_skills = True
            capture_good = False
            skills.extend([x.strip() for x in line.replace("• Skills:", "").split(",")])
        elif "Preferred" in line or "Good to have" in line:
            capture_good = True
            capture_skills = False
        elif capture_skills and line.startswith("•"):
            skills.extend([x.strip() for x in line.replace("•", "").split(",")])
        elif capture_good and line.startswith("•"):
            good_to_have.extend([x.strip() for x in line.replace("•", "").split(",")])
        elif not line.startswith("•"):
            capture_skills = False
            capture_good = False
    return skills, good_to_have

def extract_role_title(jd_file):
    """Extract role title from JD (first meaningful line)"""
    with open(jd_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line and not line.startswith("•"):
            return line
    return "Unknown Role"
