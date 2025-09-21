import glob
import fitz  # PyMuPDF
import docx2txt
import os

def extract_pdf_text(pdf_file):
    """Extract text from a PDF file using PyMuPDF."""
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
    """Extract text from a DOCX file using docx2txt."""
    try:
        return docx2txt.process(docx_file)
    except Exception as e:
        print(f"Error reading {docx_file}: {e}")
        return ""

def get_all_resumes(folder="."):
    """Get all PDF and DOCX files in the folder."""
    pdf_files = glob.glob(os.path.join(folder, "*.pdf"))
    docx_files = glob.glob(os.path.join(folder, "*.docx"))
    return pdf_files + docx_files

def parse_resumes(folder="."):
    """Parse all resumes and return a dictionary {filename: text}."""
    resumes = get_all_resumes(folder)
    parsed_data = {}
    for resume_file in resumes:
        if resume_file.lower().endswith(".pdf"):
            text = extract_pdf_text(resume_file)
        elif resume_file.lower().endswith(".docx"):
            text = extract_docx_text(resume_file)
        else:
            continue
        parsed_data[resume_file] = text
        print(f"Parsed {resume_file}: {len(text)} characters")
    return parsed_data

if __name__ == "__main__":
    folder_path = "."  # Change this if your resumes are in another folder
    parsed_resumes = parse_resumes(folder_path)
    
    # Optional: save parsed text to individual txt files
    for filename, text in parsed_resumes.items():
        clean_name = os.path.splitext(os.path.basename(filename))[0]
        with open(f"{clean_name}.txt", "w", encoding="utf-8") as f:
            f.write(text)
    print("Parsing complete. Text files saved.")
