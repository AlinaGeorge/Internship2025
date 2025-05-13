import pymupdf as fitz

def chunks(pdf_path, chunk_size):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        full_text += page.get_text()

    chunks = []
    start = 0
    if chunk_size < len(full_text):         #checks if the chunk size is less than the text length
        while start < len(full_text):       
            chunk = full_text[start:start + chunk_size]     #extracts the text of chunk size from the full text
            chunks.append(chunk)            #adds the chunk to the list
            start += chunk_size             #resets the start to the next chunk
            #doc.close()           
        return chunks
    else:
        print("Chunk size is larger than the text length.")
        return []

path=input("Enter the path of the PDF file: ")
chunk_size = int(input("Enter the chunk size: "))
print("Extracted chunks:",chunks(path,chunk_size))

