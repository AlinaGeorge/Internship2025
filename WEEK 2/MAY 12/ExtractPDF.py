import pymupdf as fitz

def extract(filepath):
    doc = fitz.open(filepath)   #open the PDF file
    text=""
    for page in doc:    #iterate through each page
        text+=page.get_text()   #store the text of each page in a variable
    doc.close()
    return text

path=input("Enter the path of the PDF file: ")
text = extract(path)
print("Extracted text:",text)