# integrated_pipeline.py

import os
import re
import numpy as np
from parse_files import parse_resumes
from parse_jds import parse_all_jds
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Load embedding model once
# -----------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')

# -----------------------------
# Hard match function
# -----------------------------
def compute_hard_match(resume_text, jd_skills):
    if not jd_skills:
        return 0
    resume_text_lower = resume_text.lower()
    matched = 0
    for skill in jd_skills:
        if skill.lower() in resume_text_lower:
            matched += 1
    score = (matched / len(jd_skills)) * 100
    return round(score, 2)

# -----------------------------
# Semantic similarity
# -----------------------------
def semantic_similarity_jd_resume(jd_skills, resume_text):
    if not jd_skills:
        return 0.0
    jd_embeddings = model.encode(jd_skills)
    resume_embedding = model.encode([resume_text])
    similarities = cosine_similarity(jd_embeddings, resume_embedding)
    avg_sim = np.mean(similarities) * 100
    return round(avg_sim, 2)

# -----------------------------
# Weighted score
# -----------------------------
def compute_weighted_score(resume_text, jd_text, jd_skills):
    hard = compute_hard_match(resume_text, jd_skills)
    semantic = semantic_similarity_jd_resume(jd_skills, resume_text)
    return round(0.5 * hard + 0.5 * semantic, 2)

# -----------------------------
# Assign verdict based on score
# -----------------------------
def assign_verdict(score):
    if score >= 70:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"

# -----------------------------
# Main pipeline
# -----------------------------
def match_resumes_to_jds(resume_folder="resumes", jd_folder="JDS"):
    resumes = parse_resumes(resume_folder)  # {filename: text}
    jd_roles = parse_all_jds(jd_folder)     # list of roles per JD file

    results = {}

    for resume_file, resume_text in resumes.items():
        resume_matches = []

        for jd_file, roles in jd_roles.items():
            for role in roles:
                jd_skills = role.get("skills", [])
                jd_text = role.get("text", "")
                score = compute_weighted_score(resume_text, jd_text, jd_skills)
                verdict = assign_verdict(score)

                # Identify missing skills
                missing_skills = [s for s in jd_skills if s.lower() not in resume_text.lower()]

                resume_matches.append({
                    "jd_file": jd_file,
                    "role_title": role.get("role_title", "Unknown Role"),
                    "score": score,
                    "verdict": verdict,
                    "missing_skills": missing_skills
                })

        results[resume_file] = resume_matches

    return results

# -----------------------------
# Run pipeline
# -----------------------------
if __name__ == "__main__":
    results = match_resumes_to_jds(resume_folder="resumes", jd_folder="JDS")

    for resume, matches in results.items():
        print(f"\n===== Resume: {resume} =====")
        for match in matches:
            print(f"JD File: {match['jd_file']}")
            print(f"Role: {match['role_title']}")
            print(f"Score: {match['score']}%")
            print(f"Verdict: {match['verdict']}")
            print(f"Missing Skills: {match['missing_skills']}")
            print("---------------------------")
