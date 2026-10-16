import io
import re

import docx
import pdfplumber


class DocumentProcessor:
    """Handle extraction of text from various document formats"""

    _SECTION_HEADING_PATTERN = re.compile(
        r"^\s*(?P<prefix>(?:(?:ARTICLE|SECTION)\s+[A-Z0-9IVX.-]+|"
        r"\d+(?:\.\d+)*[.)]?)\s*[-:.)]?\s*)?"
        r"(?P<heading>INDEMNITY|TERMINATION(?:\s+OF\s+(?:THIS\s+)?AGREEMENT)?|"
        r"GOVERNING\s+LAW|CONFIDENTIALITY|PAYMENT(?:\s+TERMS?)?)\b"
        r"(?P<tail>.*)$",
        re.IGNORECASE,
    )
    
    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_file = io.BytesIO(file_bytes)
            with pdfplumber.open(pdf_file) as pdf:
                pages = [page.extract_text() for page in pdf.pages]
            return "\n".join(page_text for page_text in pages if page_text).strip()
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    @staticmethod
    def chunk_text(text: str) -> list[str]:
        """Split contract text at major legal headings, keeping headings with their bodies."""
        chunks = []
        current_lines = []

        for line in text.splitlines():
            match = DocumentProcessor._SECTION_HEADING_PATTERN.match(line)
            if match:
                tail = match.group("tail")
                heading_is_standalone = not tail.strip()
                heading_has_separator = tail.lstrip().startswith((":", ".", "-", "\u2013"))
                heading_is_uppercase = match.group("heading").isupper()
                if (
                    match.group("prefix")
                    or heading_is_standalone
                    or heading_has_separator
                    or heading_is_uppercase
                ):
                    current_chunk = "\n".join(current_lines).strip()
                    if current_chunk:
                        chunks.append(current_chunk)
                    current_lines = [line]
                    continue

            current_lines.append(line)

        current_chunk = "\n".join(current_lines).strip()
        if current_chunk:
            chunks.append(current_chunk)
        return chunks
    
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