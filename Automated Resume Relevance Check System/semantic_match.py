from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load a local pre-trained embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')  # lightweight and fast

# Example JD and resume
jd_skills = ["Python", "Git", "SQL", "Django", "REST APIs", "Docker"]
resume_text = """
Experienced Software Engineer skilled in Python, SQL, and Git. 
Worked on REST APIs and Docker-based deployments.
"""

# Encode JD skills and resume text
jd_embeddings = model.encode(jd_skills)
resume_embedding = model.encode([resume_text])

# Compute cosine similarity
similarities = cosine_similarity(jd_embeddings, resume_embedding)

# Print results
for i, skill in enumerate(jd_skills):
    print(f"{skill}: {similarities[i][0]:.2f}")
