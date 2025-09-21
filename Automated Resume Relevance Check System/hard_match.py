import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')

# Predefined JD skills
JD_SKILLS = ['Python', 'SQL', 'Pandas', 'NumPy', 'Power BI', 'Matplotlib', 'Seaborn', 
             'Scikit-learn', 'BeautifulSoup', 'Excel', 'Tableau']

# Paths
JD_FOLDER = './JDS/'
RESUME_FOLDER = './'

stop_words = set(stopwords.words('english'))

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_skills(resume_text):
    words = set([w.lower() for w in word_tokenize(resume_text) if w.isalpha()])
    matched_skills = [skill for skill in JD_SKILLS if skill.lower() in words]
    return matched_skills

def extract_projects(resume_text):
    projects = []
    project_split = re.split(r'(projects)', resume_text, flags=re.I)
    if len(project_split) > 1:
        project_text = project_split[1]
        lines = [line.strip() for line in project_text.split('\n') if line.strip()]
        for line in lines:
            if len(line) > 5 and 'certification' not in line.lower():
                projects.append(line)
    return projects

def extract_certifications(resume_text):
    certifications = []
    cert_split = re.split(r'(certifications?)', resume_text, flags=re.I)
    if len(cert_split) > 1:
        cert_text = cert_split[1]
        lines = [line.strip() for line in cert_text.split('\n') if line.strip()]
        for line in lines:
            if len(line) > 5:
                certifications.append(line)
    return certifications

def calculate_skill_score(matched_skills):
    if not matched_skills:
        return 0
    return round(len(matched_skills) / len(JD_SKILLS) * 100, 2)

def calculate_semantic_similarity(jd_text, resume_text):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([jd_text, resume_text])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(similarity, 3)

def calculate_total_score(skill_score, semantic_score, project_bonus=5, certification_bonus=5):
    # Weighted sum: skills 70%, semantic 25%, project/cert 5%
    total = skill_score * 0.7 + semantic_score * 25 + project_bonus + certification_bonus
    return round(total, 2)

def generate_suggestions(matched_skills, projects, certifications):
    missing_skills = [skill for skill in JD_SKILLS if skill not in matched_skills]
    suggestions = []
    if missing_skills:
        suggestions.append(f"Consider learning/improving these skills: {', '.join(missing_skills)}")
    if not projects:
        suggestions.append("Add projects relevant to this JD to strengthen your profile.")
    if not certifications:
        suggestions.append("Include certifications relevant to the role to strengthen your profile.")
    return suggestions

# Main script
jd_files = [os.path.join(JD_FOLDER, f) for f in os.listdir(JD_FOLDER) if f.endswith('.txt')]
resume_files = [os.path.join(RESUME_FOLDER, f) for f in os.listdir(RESUME_FOLDER) if f.endswith('.txt') and 'JD' not in f]

print(f"Found JD files: {jd_files}")
print(f"Found Resume files: {resume_files}\n")

for jd_file in jd_files:
    jd_text = read_text_file(jd_file)
    print(f"--- Relevance for {os.path.basename(jd_file)} ---\n")
    
    for resume_file in resume_files:
        resume_text = read_text_file(resume_file)
        
        matched_skills = extract_skills(resume_text)
        projects = extract_projects(resume_text)
        certifications = extract_certifications(resume_text)
        
        skill_score = calculate_skill_score(matched_skills)
        semantic_score = calculate_semantic_similarity(jd_text, resume_text)
        # Bonus points if projects or certifications exist
        project_bonus = 5 if projects else 0
        cert_bonus = 5 if certifications else 0
        total_score = calculate_total_score(skill_score, semantic_score, project_bonus, cert_bonus)
        
        suggestions = generate_suggestions(matched_skills, projects, certifications)
        verdict = "High" if total_score > 70 else "Medium" if total_score > 40 else "Low"
        
        print(f"Resume: {os.path.basename(resume_file)}")
        print(f"Matched skills: {matched_skills} ({skill_score}%)")
        print(f"Semantic similarity: {semantic_score}")
        print(f"Projects found: {projects}")
        print(f"Certifications found: {certifications}")
        print(f"Suggestions: {suggestions}")
        print(f"Total relevance score: {total_score}")
        print(f"Verdict: {verdict}\n")

