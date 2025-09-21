import fitz  # PyMuPDF
import docx2txt

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            page_text = page.get_text()
            if page_text:
                text += page_text + "\n"
        return text
    elif file_path.endswith(".docx"):
        return docx2txt.process(file_path)
    else:
        return ""

