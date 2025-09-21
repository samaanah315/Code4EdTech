import fitz  # PyMuPDF

# Open an existing PDF (replace 'resume-1.pdf' with your actual file)
pdf_file = "resume - 1.pdf"

doc = fitz.open(pdf_file)
print(f"Number of pages: {len(doc)}")

# Print text from first page
first_page = doc[0]
print(first_page.get_text())
doc.close()
