import os
from PyPDF2 import PdfReader
from docx import Document
import textract

class FileHandler:
    def __init__(self, uploaded_file):
        self.uploaded_file = uploaded_file

    def save_file(self):
        try:
            file_path = 'temp/' + self.uploaded_file.filename
            self.uploaded_file.save(file_path)
            self.file_path = file_path
            return True
        except:
            return False

    def get_text(self):
        file_extension = self.uploaded_file.filename.rsplit('.', 1)[1].lower()
        if file_extension == 'pdf':
            return self.extract_text_from_pdf()
        elif file_extension in ['doc', 'docx']:
            return self.extract_text_from_doc()
        elif file_extension == 'txt':
            return self.extract_text_from_txt()
        else:
            return None

    def extract_text_from_pdf(self):
        pdf_reader = PdfReader(self.file_path)
        num_pages = len(pdf_reader.pages)
        text = ''
        for page in range(num_pages):
            text += pdf_reader.pages[page].extract_text()
        return text

    def extract_text_from_doc(self):
        try:
            doc = Document(self.file_path)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            text = '\n'.join(paragraphs)
            return text
        except Exception as e:
            print(f"Error extracting text from DOC/DOCX: {e}")
            return ''

    def extract_text_from_txt(self):
        text = textract.process(self.file_path)
        return text.decode('utf-8')
