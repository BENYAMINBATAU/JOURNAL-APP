"""
Reference Manager Module
Handles formatting and validation of references
"""

import re
from typing import List, Dict, Any


class ReferenceManager:
    """Manage and format references"""
    
    def __init__(self):
        self.min_year = 2014  # Minimum year for references (10 years back)
        self.apa_pattern = re.compile(
            r'^([^(]+)\((\d{4})\)\.?\s*(.+)',
            re.IGNORECASE
        )
    
    def format_references(self, references: List[str], min_count: int = 15) -> List[str]:
        """
        Format and filter references
        
        Args:
            references: List of raw references
            min_count: Minimum number of references required
            
        Returns:
            List of formatted references
        """
        formatted_refs = []
        
        for ref in references:
            # Clean reference
            ref_clean = self._clean_reference(ref)
            
            if ref_clean and len(ref_clean) > 20:  # Skip very short refs
                formatted_refs.append(ref_clean)
        
        # Sort alphabetically by author
        formatted_refs.sort(key=lambda x: x.split('.')[0] if '.' in x else x)
        
        # Ensure minimum count
        if len(formatted_refs) < min_count:
            print(f"Warning: Only {len(formatted_refs)} references found. Minimum required: {min_count}")
        
        return formatted_refs
    
    def validate_references(self, references: List[str]) -> Dict[str, Any]:
        """
        Validate references against journal requirements
        
        Args:
            references: List of references
            
        Returns:
            Validation result dictionary
        """
        validation = {
            'total_count': len(references),
            'recent_count': 0,  # Last 10 years
            'journal_count': 0,
            'apa_compliant': 0,
            'issues': [],
            'recommendations': []
        }
        
        current_year = 2026  # Hardcoded for consistency
        
        for i, ref in enumerate(references, 1):
            # Check year
            year_match = re.search(r'\((\d{4})\)', ref)
            if year_match:
                year = int(year_match.group(1))
                if year >= self.min_year:
                    validation['recent_count'] += 1
                else:
                    validation['issues'].append(f"Reference {i}: Year {year} is too old (minimum {self.min_year})")
            else:
                validation['issues'].append(f"Reference {i}: No year found")
            
            # Check if journal (contains journal indicators)
            if re.search(r'journal|jurnal|proceedings|conference', ref, re.IGNORECASE):
                validation['journal_count'] += 1
            
            # Check APA format
            if self._is_apa_format(ref):
                validation['apa_compliant'] += 1
            else:
                validation['issues'].append(f"Reference {i}: Not in APA format")
        
        # Calculate percentages
        if validation['total_count'] > 0:
            recent_pct = (validation['recent_count'] / validation['total_count']) * 100
            journal_pct = (validation['journal_count'] / validation['total_count']) * 100
            apa_pct = (validation['apa_compliant'] / validation['total_count']) * 100
            
            # Add recommendations
            if validation['total_count'] < 15:
                validation['recommendations'].append(f"Add {15 - validation['total_count']} more references (minimum 15 required)")
            
            if recent_pct < 80:
                validation['recommendations'].append(f"Increase recent references to 80% (currently {recent_pct:.1f}%)")
            
            if journal_pct < 80:
                validation['recommendations'].append(f"Increase journal references to 80% (currently {journal_pct:.1f}%)")
            
            if apa_pct < 90:
                validation['recommendations'].append(f"Fix APA formatting (currently {apa_pct:.1f}% compliant)")
        
        validation['is_valid'] = (
            validation['total_count'] >= 15 and
            len(validation['recommendations']) == 0
        )
        
        return validation
    
    def _clean_reference(self, ref: str) -> str:
        """Clean and normalize reference"""
        # Remove leading numbers or bullets
        ref = re.sub(r'^\s*[\[\(]?\d+[\]\)]?\s*', '', ref)
        ref = re.sub(r'^\s*[•\-\*]\s*', '', ref)
        
        # Normalize spaces
        ref = re.sub(r'\s+', ' ', ref)
        
        # Ensure ends with period
        ref = ref.strip()
        if ref and not ref.endswith('.'):
            ref += '.'
        
        return ref
    
    def _is_apa_format(self, ref: str) -> bool:
        """Check if reference follows APA format"""
        # Basic APA pattern: Author(s). (Year). Title...
        
        # Check for year in parentheses
        if not re.search(r'\(\d{4}\)', ref):
            return False
        
        # Check for period after author name(s)
        if not re.search(r'^[^(]+\(\d{4}\)', ref):
            return False
        
        return True
    
    def convert_to_apa(self, ref: str) -> str:
        """
        Attempt to convert reference to APA format
        
        Args:
            ref: Reference string
            
        Returns:
            APA-formatted reference (best effort)
        """
        # This is a simplified conversion
        # In production, would use more sophisticated parsing
        
        # Already in APA format
        if self._is_apa_format(ref):
            return ref
        
        # Try to extract components
        year_match = re.search(r'\b(19|20)\d{2}\b', ref)
        
        if year_match:
            year = year_match.group(0)
            before_year = ref[:year_match.start()].strip()
            after_year = ref[year_match.end():].strip()
            
            # Reconstruct in APA format
            if before_year:
                # Remove trailing punctuation from author
                author = re.sub(r'[,\.;]+$', '', before_year)
                
                # Format: Author. (Year). Rest.
                apa_ref = f"{author}. ({year}). {after_year}"
                
                # Ensure ends with period
                if not apa_ref.endswith('.'):
                    apa_ref += '.'
                
                return apa_ref
        
        # Could not convert, return original
        return ref
    
    def generate_sample_references(self, count: int = 15) -> List[str]:
        """
        Generate sample references for testing
        
        Args:
            count: Number of references to generate
            
        Returns:
            List of sample references
        """
        samples = [
            "Anderson, J. R., & Lebiere, C. (2014). The atomic components of thought. Lawrence Erlbaum Associates.",
            "Brown, P., Smith, K., & Johnson, M. (2018). Advances in machine learning. Journal of AI Research, 45(2), 123-145.",
            "Chen, X., Wang, Y., & Li, Z. (2020). Deep learning applications in education. Educational Technology Review, 28(3), 234-256.",
            "Davis, R. (2019). Research methodology in social sciences (3rd ed.). Academic Press.",
            "Evans, M., & Wilson, T. (2021). Data analysis techniques. Statistical Methods Quarterly, 15(4), 567-589.",
            "Fischer, K., Mueller, H., & Schmidt, P. (2017). Cognitive psychology fundamentals. European Journal of Psychology, 23(1), 45-67.",
            "Garcia, L., Martinez, A., & Rodriguez, C. (2022). Educational innovation strategies. International Education Journal, 34(2), 178-192.",
            "Harris, D., & Thompson, J. (2020). Qualitative research methods. Research Quarterly, 19(3), 301-325.",
            "Ibrahim, A., & Rahman, M. (2023). Technology in higher education. Asian Journal of Educational Technology, 12(1), 89-103.",
            "Jones, S., Williams, R., & Taylor, B. (2019). Learning theories and practice. Educational Psychology Review, 31(4), 445-467.",
            "Kumar, V., & Patel, S. (2021). Digital transformation in education. Technology & Learning, 25(2), 156-178.",
            "Lee, H., Kim, S., & Park, J. (2018). Assessment and evaluation methods. Assessment in Education, 22(3), 289-311.",
            "Morrison, K., & Bell, A. (2020). Collaborative learning environments. Journal of Collaborative Education, 16(1), 67-89.",
            "Nelson, P., & Carter, M. (2022). Student engagement strategies. Higher Education Quarterly, 38(4), 412-434.",
            "O'Brien, T., & Murphy, C. (2023). Innovative teaching approaches. Teaching and Teacher Education, 41(2), 234-256.",
        ]
        
        return samples[:count]
