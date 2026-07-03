# pdf_processor.py
from pypdf import PdfReader
import re

def extract_and_chunk_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    chunks_with_pages = []
    
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() + "\n"
        sentences = re.split(r'(?<=[\.\?\!])\s+', text)
        
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < 400:
                current_chunk += " " + sentence
            else:
                if current_chunk.strip():
                    chunks_with_pages.append({
                        "text": current_chunk.strip(),
                        "page": page_num
                    })
                current_chunk = sentence
        if current_chunk.strip():
            chunks_with_pages.append({
                "text": current_chunk.strip(),
                "page": page_num
            })
            
    return chunks_with_pages