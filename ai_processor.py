"""
AI Processor Module
Handles AI-powered content enhancement using Claude or GPT-4
"""

import os
from typing import Dict, Any, Optional
from anthropic import Anthropic
from openai import OpenAI


class AIProcessor:
    """AI-powered content enhancement"""
    
    def __init__(self, provider: str = 'claude'):
        """
        Initialize AI processor
        
        Args:
            provider: 'claude' or 'gpt4'
        """
        self.provider = provider
        
        if provider == 'claude':
            api_key = os.environ.get('ANTHROPIC_API_KEY')
            if api_key:
                self.client = Anthropic(api_key=api_key)
            else:
                self.client = None
                print("Warning: ANTHROPIC_API_KEY not set. AI features disabled.")
        
        elif provider == 'gpt4':
            api_key = os.environ.get('OPENAI_API_KEY')
            if api_key:
                self.client = OpenAI(api_key=api_key)
            else:
                self.client = None
                print("Warning: OPENAI_API_KEY not set. AI features disabled.")
    
    def enhance_content(self, thesis_content: Dict[str, Any], settings: Dict) -> Dict[str, Any]:
        """
        Enhance thesis content using AI
        
        Args:
            thesis_content: Extracted thesis content
            settings: Processing settings
            
        Returns:
            Enhanced thesis content
        """
        if not self.client:
            print("AI client not available, skipping enhancement")
            return thesis_content
        
        try:
            # Enhance abstract
            if thesis_content.get('abstract_en'):
                thesis_content['abstract_en'] = self.enhance_abstract(
                    thesis_content['abstract_en'], 'english'
                )
            
            if thesis_content.get('abstract_id'):
                thesis_content['abstract_id'] = self.enhance_abstract(
                    thesis_content['abstract_id'], 'indonesian'
                )
            
            # Generate keywords
            thesis_content['keywords_en'] = self.generate_keywords(
                thesis_content.get('title', '') + ' ' + thesis_content.get('abstract_en', ''),
                'english'
            )
            
            thesis_content['keywords_id'] = self.generate_keywords(
                thesis_content.get('title', '') + ' ' + thesis_content.get('abstract_id', ''),
                'indonesian'
            )
            
            # Summarize methodology
            if thesis_content.get('methodology'):
                thesis_content['methodology_summary'] = self.summarize_section(
                    thesis_content['methodology'],
                    section_type='methodology',
                    max_words=300
                )
            
            # Summarize results
            if thesis_content.get('results'):
                thesis_content['results_summary'] = self.summarize_section(
                    thesis_content['results'],
                    section_type='results',
                    max_words=400
                )
            
            # Enhance conclusions
            if thesis_content.get('conclusions'):
                thesis_content['conclusions_summary'] = self.summarize_section(
                    thesis_content['conclusions'],
                    section_type='conclusions',
                    max_words=200
                )
            
        except Exception as e:
            print(f"Error enhancing content with AI: {str(e)}")
        
        return thesis_content
    
    def enhance_abstract(self, text: str, language: str = 'english') -> str:
        """Enhance abstract quality"""
        if not text or not self.client:
            return text
        
        prompt = self._build_abstract_prompt(text, language)
        
        try:
            if self.provider == 'claude':
                response = self.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
            
            elif self.provider == 'gpt4':
                response = self.client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000
                )
                return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error enhancing abstract: {str(e)}")
            return text
    
    def generate_keywords(self, text: str, language: str = 'english', count: int = 5) -> str:
        """Generate keywords from text"""
        if not text or not self.client:
            return ''
        
        lang_name = 'English' if language == 'english' else 'Indonesian'
        
        prompt = f"""Extract {count} most relevant keywords from the following text in {lang_name}.
        
Return ONLY the keywords separated by commas, nothing else.

Text:
{text[:2000]}

Keywords:"""
        
        try:
            if self.provider == 'claude':
                response = self.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=100,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
            
            elif self.provider == 'gpt4':
                response = self.client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=100
                )
                return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating keywords: {str(e)}")
            return ''
    
    def summarize_section(self, text: str, section_type: str, max_words: int = 300) -> str:
        """Summarize a section for journal article"""
        if not text or not self.client:
            return text[:max_words * 6]  # Rough character estimate
        
        prompt = f"""Summarize the following {section_type} section from a thesis into a concise paragraph suitable for a journal article (maximum {max_words} words).

Focus on:
- Key points and findings
- Methodology or approach (if applicable)
- Main conclusions or implications

Text to summarize:
{text[:3000]}

Summary:"""
        
        try:
            if self.provider == 'claude':
                response = self.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=max_words * 2,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
            
            elif self.provider == 'gpt4':
                response = self.client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_words * 2
                )
                return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error summarizing section: {str(e)}")
            return text[:max_words * 6]
    
    def _build_abstract_prompt(self, text: str, language: str) -> str:
        """Build prompt for abstract enhancement"""
        lang_name = 'English' if language == 'english' else 'Indonesian'
        
        return f"""Improve the following research abstract for a journal article in {lang_name}.

Requirements:
- Keep it between 150-250 words
- Clear structure: background, objectives, methods, results, conclusions
- Use academic language
- Keep all specific findings and data
- Do NOT add information not in the original text

Original abstract:
{text}

Enhanced abstract:"""
