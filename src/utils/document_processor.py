import PyPDF2
import docx
from typing import Optional
import io

class DocumentProcessor:
    """Handle extraction of text from various document formats"""
    
    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_file = io.BytesIO(file_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(file_bytes: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            docx_file = io.BytesIO(file_bytes)
            doc = docx.Document(docx_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {str(e)}")
    
    @staticmethod
    def extract_text_from_txt(file_bytes: bytes) -> str:
        """Extract text from TXT file"""
        try:
            return file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                return file_bytes.decode('latin-1')
            except Exception as e:
                raise Exception(f"Error extracting text from TXT: {str(e)}")
    
    @staticmethod
    def process_document(uploaded_file) -> str:
        """Process uploaded document and extract text"""
        file_bytes = uploaded_file.read()
        file_name = uploaded_file.name.lower()
        
        if file_name.endswith('.pdf'):
            return DocumentProcessor.extract_text_from_pdf(file_bytes)
        elif file_name.endswith('.docx'):
            return DocumentProcessor.extract_text_from_docx(file_bytes)
        elif file_name.endswith('.txt'):
            return DocumentProcessor.extract_text_from_txt(file_bytes)
        else:
            raise ValueError("Unsupported file format. Please upload PDF, DOCX, or TXT files.")
    
    @staticmethod
    def detect_language(text: str) -> str:
        """Simple language detection for English/Hindi"""
        # Count Devanagari characters
        hindi_chars = sum(1 for char in text if '\u0900' <= char <= '\u097F')
        total_chars = len(text.replace(" ", "").replace("\n", ""))
        
        if total_chars == 0:
            return "unknown"
        
        hindi_ratio = hindi_chars / total_chars
        
        if hindi_ratio > 0.3:
            return "hindi"
        else:
            return "english"