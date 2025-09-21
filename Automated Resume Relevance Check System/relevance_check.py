import os
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ensure nltk packages are downloaded
nltk.download('punkt')
nltk.download('stopwords')

# -----------------------
# Utility Functions
# -----------------------

def clean_text(text):
    """Lowercase, remove special characters, and tokenize"""
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in stopwords.words('english')]
    return ' '.join(tokens)

def extract_projects(resume_text):
    """Extract projects with name + description cleanly"""
    projects_section = re.split(r'\bProjects\b|\bPROJECTS\b', resume_text, flags=re.IGNORECASE)
    projects = []

    if len(projects_section) > 1:
        project_text = projects_section[1]
        lines = [line.strip() for line in project_text.split('\n') if line.strip()]
        
        current_project_name = None
        current_project_desc = []

        for line in lines:
            # Detect a new project title if it ends with ':' or is a short capitalized line
            if (line.endswith(':') or (len(line.split()) < 12 and line[0].isupper())):
                if current_project_name:
                    projects.append({
                        'project_name': current_project_name.rstrip(':'),
                        'description': ' '.join(current_project_desc)
                    })
                current_project_name = line
                current_project_desc = []
            else:
                current_project_desc.append(line)
        # Append the last project
        if current_project_name:
            projects.append({
                'project_name': current_project_name.rstrip(':'),
                'description': ' '.join(current_project_desc)
            })
    return projects

def extract_certifications(resume_text):
    """Extract certifications cleanly"""
    cert_section = re.split(r'\bCertifications\b|\bCERTIFICATIONS\b', resume_text, flags=re.IGNORECASE)
    certifications = []

    if len(cert_section) > 1:
        cert_text = cert_section[1]
        lines = [line.strip() for line in cert_text.split('\n') if line.strip()]
        for line in lines:
            # Remove bullets and short lines
            clean_line = re.sub(r'^[\u2022\-\*\s]+', '', line)
            if len(clean_line) > 5:
                certifications.append(clean_line)
    return certifications

def calculate_relevance(resume_text, jd_text, skills_list):
    """Calculate skill match, semantic similarity, and extract projects/certifications"""
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)

    # Skill Matching
    matched_skills = [skill for skill in skills_list if skill.lower() in resume_clean]
    skill_score = 0
    if matched_skills:
        skill_score = 100 * len(matched_skills) / len(skills_list)

    # Semantic similarity
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([resume_clean, jd_clean])
    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

    # Projects and Certifications
    projects = extract_projects(resume_text)
    certifications = extract_certifications(resume_text)

    # Suggestions
    suggestions = []
    if skill_score < 100:
        missing_skills = [skill for skill in skills_list if skill not in matched_skills]
        suggestions.append(f"Consider learning/improving these skills: {', '.join(missing_skills)}")
    if not projects:
        suggestions.append("Add projects relevant to this JD to strengthen your profile.")
    if not certifications:
        suggestions.append("Include certifications relevant to the role to strengthen your profile.")

    # Total relevance score (weighted sum example)
    total_score = skill_score + similarity * 100
    verdict = "High" if total_score > 50 else "Low"

    return {
        'matched_skills': matched_skills,
        'skill_score': round(skill_score, 2),
        'semantic_similarity': round(similarity, 4),
        'projects': projects,
        'certifications': certifications,
        'suggestions': suggestions,
        'total_score': round(total_score, 2),
        'verdict': verdict
    }

# -----------------------
# Main Execution
# -----------------------

def main():
    # Paths
    jd_folder = './JDS'
    resume_folder = '.'

    # Skills list
    skills_list = ['Python', 'SQL', 'Pandas', 'NumPy', 'Power BI', 'Matplotlib', 'Seaborn', 'Scikit-learn', 'Excel', 'BeautifulSoup', 'Tableau']

    # Get JD files
    jd_files = [os.path.join(jd_folder, f) for f in os.listdir(jd_folder) if f.endswith('.txt')]
    print("Found JD files:", jd_files)

    # Get Resume files
    resume_files = [os.path.join(resume_folder, f) for f in os.listdir(resume_folder) if f.endswith('.txt') and 'JD' not in f]
    print("Found Resume files:", resume_files)

    # Loop through each JD and Resume
    for jd_file in jd_files:
        with open(jd_file, 'r', encoding='utf-8') as f:
            jd_text = f.read()
        print(f"\n--- Relevance for {os.path.basename(jd_file)} ---\n")
        for resume_file in resume_files:
            with open(resume_file, 'r', encoding='utf-8') as f:
                resume_text = f.read()
            result = calculate_relevance(resume_text, jd_text, skills_list)
            print(f"Resume: {os.path.basename(resume_file)}")
            print(f"Matched skills: {result['matched_skills']} ({result['skill_score']}%)")
            print(f"Semantic similarity: {result['semantic_similarity']}")
            print("Projects found:")
            for p in result['projects']:
                print(f"  - {p['project_name']}: {p['description']}")
            print(f"Certifications found: {result['certifications']}")
            print(f"Suggestions: {result['suggestions']}")
            print(f"Total relevance score: {result['total_score']}")
            print(f"Verdict: {result['verdict']}\n")

if __name__ == "__main__":
    main()

