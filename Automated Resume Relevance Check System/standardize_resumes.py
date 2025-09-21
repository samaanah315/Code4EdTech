# standardize_resumes.py
import fitz  # PyMuPDF
import docx2txt
import re
import os

# ---------- Step 1: Functions to extract raw text ----------

def extract_pdf_text(pdf_file):
    text = ""
    try:
        doc = fitz.open(pdf_file)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"Error reading {pdf_file}: {e}")
    return text

def extract_docx_text(docx_file):
    try:
        return docx2txt.process(docx_file)
    except Exception as e:
        print(f"Error reading {pdf_file}: {e}")
        return ""

# ---------- Step 2: Standardize the text ----------

def standardize_resume_text(raw_text):
    text = raw_text
    text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)
    lines = text.split('\n')
    lines = [line.strip() for line in lines if len(line.strip()) > 2]
    text = '\n'.join(lines)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('•', '-').replace('·', '-').replace('*', '-')
    section_keywords = ['skills', 'education', 'experience', 'projects', 'certifications']
    for keyword in section_keywords:
        text = re.sub(keyword, keyword.upper(), text, flags=re.IGNORECASE)
    return text

# ---------- Step 3: Process all resumes in folder ----------
if __name__ == "__main__":
    resume_folder = "./resumes"  # folder where your PDF/DOCX files are
    output_folder = "./resumes_clean"  # folder to save cleaned text files

    os.makedirs(output_folder, exist_ok=True)

    # List all PDFs and DOCXs
    resumes = [f for f in os.listdir(resume_folder) if f.lower().endswith((".pdf", ".docx"))]

    for resume_file in resumes:
        file_path = os.path.join(resume_folder, resume_file)
        if resume_file.lower().endswith(".pdf"):
            raw_text = extract_pdf_text(file_path)
        else:
            raw_text = extract_docx_text(file_path)

        cleaned_text = standardize_resume_text(raw_text)
        clean_name = os.path.splitext(resume_file)[0] + "_clean.txt"
        clean_path = os.path.join(output_folder, clean_name)

        with open(clean_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

        print(f"Saved standardized file: {clean_path}")

    print("All resumes standardized and saved.")

