import pymupdf as fitz

def extract(filepath):
    doc = fitz.open(filepath)
    text=""
    for page in doc:
        text+=page.get_text()
    doc.close()
    return text

path=input("Enter the path of the PDF file: ")
text = extract(path)
print("Extracted text:",text)