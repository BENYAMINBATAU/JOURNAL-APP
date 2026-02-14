"""
Document Processor Module
Handles extraction of content from PDF and DOCX files
"""

import os
import re
from typing import List, Dict, Any
import pdfplumber
from docx import Document
import mammoth
from bs4 import BeautifulSoup


class DocumentProcessor:
    """Process and extract content from thesis documents"""
    
    def __init__(self):
        self.supported_formats = ['pdf', 'docx', 'doc']
    
    def extract_thesis_content(self, files: List[Dict]) -> Dict[str, Any]:
        """
        Extract structured content from thesis files
        
        Args:
            files: List of file dictionaries with filepath and type
            
        Returns:
            Dictionary with extracted thesis content
        """
        thesis_content = {
            'title': '',
            'author': '',
            'abstract_en': '',
            'abstract_id': '',
            'chapters': {},
            'references': [],
            'raw_text': '',
            'metadata': {}
        }
        
        # Sort files by type and name
        files_sorted = self._sort_files(files)
        
        # Extract from each file
        for file_info in files_sorted:
            content = self._extract_from_file(file_info)
            thesis_content = self._merge_content(thesis_content, content, file_info)
        
        # Post-process content
        thesis_content = self._post_process(thesis_content)
        
        return thesis_content
    
    def _sort_files(self, files: List[Dict]) -> List[Dict]:
        """Sort files by likely order (cover, chapters, references)"""
        priority_keywords = {
            'sampul': 0, 'cover': 0,
            'bab_i': 1, 'bab_1': 1, 'chapter_1': 1,
            'bab_ii': 2, 'bab_2': 2, 'chapter_2': 2,
            'bab_iii': 3, 'bab_3': 3, 'chapter_3': 3,
            'bab_iv': 4, 'bab_4': 4, 'chapter_4': 4,
            'bab_v': 5, 'bab_5': 5, 'chapter_5': 5,
            'daftar_pustaka': 6, 'references': 6, 'bibliography': 6
        }
        
        def get_priority(filename):
            filename_lower = filename.lower()
            for keyword, priority in priority_keywords.items():
                if keyword in filename_lower:
                    return priority
            return 99
        
        return sorted(files, key=lambda x: get_priority(x['filename']))
    
    def _extract_from_file(self, file_info: Dict) -> Dict[str, Any]:
        """Extract content from a single file"""
        filepath = file_info['filepath']
        file_type = file_info['type']
        
        if file_type == 'pdf':
            return self._extract_from_pdf(filepath)
        elif file_type in ['docx', 'doc']:
            return self._extract_from_docx(filepath)
        else:
            return {'text': '', 'structure': {}}
    
    def _extract_from_pdf(self, filepath: str) -> Dict[str, Any]:
        """Extract text and structure from PDF"""
        content = {
            'text': '',
            'structure': {},
            'pages': []
        }
        
        try:
            with pdfplumber.open(filepath) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text() or ''
                    content['pages'].append(text)
                    content['text'] += text + '\n\n'
            
            # Detect structure
            content['structure'] = self._detect_structure(content['text'])
            
        except Exception as e:
            print(f"Error extracting PDF {filepath}: {str(e)}")
        
        return content
    
    def _extract_from_docx(self, filepath: str) -> Dict[str, Any]:
        """Extract text and structure from DOCX"""
        content = {
            'text': '',
            'structure': {},
            'paragraphs': []
        }
        
        try:
            # Try python-docx first
            doc = Document(filepath)
            
            for para in doc.paragraphs:
                text = para.text.strip()
                if text:
                    content['paragraphs'].append({
                        'text': text,
                        'style': para.style.name if para.style else 'Normal',
                        'level': self._get_heading_level(para)
                    })
                    content['text'] += text + '\n\n'
            
            # Detect structure
            content['structure'] = self._detect_structure(content['text'])
            
        except Exception as e:
            print(f"Error extracting DOCX {filepath}: {str(e)}")
            # Fallback to mammoth
            try:
                with open(filepath, 'rb') as docx_file:
                    result = mammoth.convert_to_html(docx_file)
                    html = result.value
                    soup = BeautifulSoup(html, 'html.parser')
                    content['text'] = soup.get_text()
                    content['structure'] = self._detect_structure(content['text'])
            except:
                pass
        
        return content
    
    def _get_heading_level(self, paragraph) -> int:
        """Get heading level from paragraph style"""
        style_name = paragraph.style.name.lower() if paragraph.style else ''
        
        if 'heading 1' in style_name or 'title' in style_name:
            return 1
        elif 'heading 2' in style_name:
            return 2
        elif 'heading 3' in style_name:
            return 3
        
        return 0
    
    def _detect_structure(self, text: str) -> Dict[str, Any]:
        """Detect document structure from text"""
        structure = {
            'has_abstract': False,
            'has_chapters': False,
            'chapter_markers': [],
            'sections': []
        }
        
        # Detect abstract
        if re.search(r'abstract|abstrak', text, re.IGNORECASE):
            structure['has_abstract'] = True
        
        # Detect chapters
        chapter_pattern = r'(?:BAB|CHAPTER)\s+(?:[IVX]+|\d+)'
        chapters = re.finditer(chapter_pattern, text, re.IGNORECASE)
        structure['chapter_markers'] = [m.group() for m in chapters]
        structure['has_chapters'] = len(structure['chapter_markers']) > 0
        
        # Detect sections
        section_patterns = [
            r'pendahuluan',
            r'latar\s+belakang',
            r'tinjauan\s+pustaka',
            r'kajian\s+pustaka',
            r'metode\s+penelitian',
            r'hasil\s+dan\s+pembahasan',
            r'hasil\s+penelitian',
            r'pembahasan',
            r'kesimpulan',
            r'simpulan',
            r'saran',
            r'daftar\s+pustaka',
            r'referensi'
        ]
        
        for pattern in section_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                structure['sections'].append(pattern.replace('\\s+', ' '))
        
        return structure
    
    def _merge_content(self, thesis: Dict, new_content: Dict, file_info: Dict) -> Dict:
        """Merge new content into thesis structure"""
        filename = file_info['filename'].lower()
        text = new_content.get('text', '')
        
        # Detect file purpose
        if 'sampul' in filename or 'cover' in filename:
            thesis['title'], thesis['author'] = self._extract_title_author(text)
        
        elif 'bab_i' in filename or 'bab_1' in filename or 'chapter_1' in filename:
            thesis['chapters']['bab_i'] = text
            # Extract background
            thesis['background'] = self._extract_section(text, 'latar belakang')
            thesis['objectives'] = self._extract_section(text, 'tujuan penelitian')
        
        elif 'bab_ii' in filename or 'bab_2' in filename or 'chapter_2' in filename:
            thesis['chapters']['bab_ii'] = text
            thesis['literature_review'] = text
        
        elif 'bab_iii' in filename or 'bab_3' in filename or 'chapter_3' in filename:
            thesis['chapters']['bab_iii'] = text
            thesis['methodology'] = text
        
        elif 'bab_iv' in filename or 'bab_4' in filename or 'chapter_4' in filename:
            thesis['chapters']['bab_iv'] = text
            thesis['results'] = text
        
        elif 'bab_v' in filename or 'bab_5' in filename or 'chapter_5' in filename:
            thesis['chapters']['bab_v'] = text
            thesis['conclusions'] = self._extract_section(text, 'simpulan|kesimpulan')
        
        elif 'daftar' in filename or 'pustaka' in filename or 'reference' in filename:
            thesis['references'] = self._extract_references(text)
        
        # Accumulate raw text
        thesis['raw_text'] += text + '\n\n'
        
        return thesis
    
    def _extract_title_author(self, text: str) -> tuple:
        """Extract title and author from cover page"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        title = ''
        author = ''
        
        # Title usually in first few lines (not including university name)
        for i, line in enumerate(lines[:10]):
            if len(line) > 20 and not re.search(r'universitas|university|sekolah|institut', line, re.IGNORECASE):
                if not title and len(line.split()) > 3:
                    title = line
                    break
        
        # Author usually before NIM/student number
        for i, line in enumerate(lines):
            if re.search(r'\d{9,}', line):  # Student number pattern
                if i > 0:
                    author = lines[i-1]
                break
        
        return title, author
    
    def _extract_section(self, text: str, section_name: str) -> str:
        """Extract specific section from text"""
        pattern = rf'{section_name}(.*?)(?:(?:BAB|CHAPTER|\d+\.\d+)|$)'
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        return ''
    
    def _extract_references(self, text: str) -> List[str]:
        """Extract references from bibliography"""
        references = []
        
        # Split by common reference separators
        lines = text.split('\n')
        
        current_ref = ''
        for line in lines:
            line = line.strip()
            
            # Skip headers
            if re.match(r'^daftar\s+pustaka|^references|^bibliography', line, re.IGNORECASE):
                continue
            
            # Check if new reference (starts with author name pattern or number)
            if re.match(r'^[\[\(]?\d+[\]\)]?|^[A-Z][a-z]+,?\s+[A-Z]', line):
                if current_ref:
                    references.append(current_ref.strip())
                current_ref = line
            else:
                if current_ref and line:
                    current_ref += ' ' + line
        
        # Add last reference
        if current_ref:
            references.append(current_ref.strip())
        
        return references
    
    def _post_process(self, thesis: Dict) -> Dict:
        """Post-process extracted content"""
        # Clean up text
        if 'raw_text' in thesis:
            thesis['raw_text'] = self._clean_text(thesis['raw_text'])
        
        # Extract abstracts if not already extracted
        if not thesis.get('abstract_en'):
            thesis['abstract_en'] = self._extract_abstract(thesis['raw_text'], 'english')
        
        if not thesis.get('abstract_id'):
            thesis['abstract_id'] = self._extract_abstract(thesis['raw_text'], 'indonesian')
        
        # Generate metadata
        thesis['metadata'] = {
            'word_count': len(thesis['raw_text'].split()),
            'chapter_count': len(thesis.get('chapters', {})),
            'reference_count': len(thesis.get('references', [])),
            'has_methodology': bool(thesis.get('methodology')),
            'has_results': bool(thesis.get('results'))
        }
        
        return thesis
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        
        # Normalize line breaks
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def _extract_abstract(self, text: str, language: str) -> str:
        """Extract abstract from text"""
        if language == 'english':
            pattern = r'(?:ABSTRACT|Abstract)(.*?)(?:Keywords|KEYWORDS|ABSTRAK|Abstrak|CHAPTER|BAB)'
        else:
            pattern = r'(?:ABSTRAK|Abstrak)(.*?)(?:Kata Kunci|Kata kunci|CHAPTER|BAB|LATAR)'
        
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        
        if match:
            abstract = match.group(1).strip()
            # Limit to reasonable length
            words = abstract.split()
            if len(words) > 500:
                abstract = ' '.join(words[:500]) + '...'
            return abstract
        
        return ''
