"""
LangChain OutputParser for ResponseFormatter
Integrates ResponseFormatter into LangChain chain with structured output
"""
import re
from typing import Dict, Any
from langchain_core.output_parsers import BaseOutputParser
from pydantic import Field

try:
    # Try relative imports first (for Vercel serverless)
    from .response_formatter import ResponseFormatter
except ImportError:
    # Fallback to absolute imports (for local development)
    from response_formatter import ResponseFormatter


class FormattedOutputParser(BaseOutputParser[Dict[str, Any]]):
    """
    LangChain OutputParser that formats LLM responses according to admin-selected style.
    
    Returns structured output:
    - final_text: Formatted response text
    - tokens_used: Approximate token count (words * 1.3)
    - truncated: Whether response was truncated to sentence limits
    """
    
    style: str = Field(default="short", description="Response style: 'short' or 'conversational'")
    user_input: str = Field(default="", description="Original user input for context")
    
    def __init__(self, style: str = "short", user_input: str = "", **kwargs):
        """
        Initialize the parser.
        
        Args:
            style: Response style ("short" or "conversational")
            user_input: Original user input for context (e.g., greeting detection)
        """
        super().__init__(style=style, user_input=user_input, **kwargs)
    
    def parse(self, text: str) -> Dict[str, Any]:
        """
        Parse and format LLM output.
        
        Args:
            text: Raw LLM response text
            
        Returns:
            Dictionary with:
                - final_text: Formatted response
                - tokens_used: Approximate token count
                - truncated: Boolean indicating if response was truncated
        """
        if not text or not text.strip():
            # Fallback for empty response
            return {
                "final_text": "I don't have enough information to answer that. Could you rephrase your question?",
                "tokens_used": 15,
                "truncated": False
            }
        
        original_text = text.strip()
        
        # Step 1: Remove code fences unless user asked for code/examples
        code_requested = self._user_wants_code()
        if not code_requested:
            original_text = self._remove_code_fences(original_text)
        
        # Step 2: Check if response is useful
        if not self._is_useful_response(original_text):
            # Fallback to clarification question
            return {
                "final_text": "Could you please provide more details about what you're looking for?",
                "tokens_used": 12,
                "truncated": False
            }
        
        # Step 3: Apply ResponseFormatter
        formatter = ResponseFormatter(style=self.style)
        formatted_text = formatter.format(original_text, self.user_input)
        
        # Step 4: Calculate if response was truncated
        original_sentences = self._count_sentences(original_text)
        final_sentences = self._count_sentences(formatted_text)
        max_sentences = 2 if self.style == "short" else 3
        
        was_truncated = original_sentences > max_sentences or len(formatted_text) < len(original_text) * 0.5
        
        # Step 5: Calculate approximate token count
        tokens = self._estimate_tokens(formatted_text)
        
        return {
            "final_text": formatted_text,
            "tokens_used": tokens,
            "truncated": was_truncated
        }
    
    def _remove_code_fences(self, text: str) -> str:
        """
        Remove code fences (```...```) from text.
        
        Args:
            text: Input text
            
        Returns:
            Text with code fences removed
        """
        # Remove code blocks with language specifiers
        text = re.sub(r'```[\w]*\n.*?```', '', text, flags=re.DOTALL)
        
        # Remove inline code
        text = re.sub(r'`([^`]+)`', r'\1', text)
        
        return text
    
    def _user_wants_code(self) -> bool:
        """
        Check if user is asking for code or examples.
        
        Returns:
            True if user wants code/examples
        """
        code_keywords = ['code', 'example', 'snippet', 'script', 'command', 'syntax', 'implementation']
        user_lower = self.user_input.lower()
        return any(keyword in user_lower for keyword in code_keywords)
    
    def _is_useful_response(self, text: str) -> bool:
        """
        Check if the response contains useful information.
        
        Args:
            text: Response text
            
        Returns:
            True if response is useful
        """
        # Check minimum length
        if len(text.strip()) < 10:
            return False
        
        # Check for common "I don't know" patterns
        unhelpful_patterns = [
            r"I (?:don't|do not) know",
            r"I (?:don't|do not) have (?:that|this|the) information",
            r"I (?:can't|cannot) (?:help|answer|provide)",
            r"I'm (?:not sure|unable)",
            r"(?:Sorry|Apologies),? (?:I|but I)",
        ]
        
        for pattern in unhelpful_patterns:
            if re.search(pattern, text, flags=re.IGNORECASE):
                # If entire response is just the unhelpful message, consider it not useful
                if len(text.strip()) < 100:
                    return False
        
        return True
    
    def _count_sentences(self, text: str) -> int:
        """
        Count sentences in text.
        
        Args:
            text: Input text
            
        Returns:
            Number of sentences
        """
        # Split on sentence endings
        sentences = re.split(r'[.!?]+', text)
        # Filter empty strings
        sentences = [s.strip() for s in sentences if s.strip()]
        return len(sentences)
    
    def _estimate_tokens(self, text: str) -> int:
        """
        Estimate token count (rough approximation: words * 1.3).
        
        Args:
            text: Input text
            
        Returns:
            Estimated token count
        """
        words = len(text.split())
        # Rough token estimate: 1 word ≈ 1.3 tokens on average
        return int(words * 1.3)
    
    @property
    def _type(self) -> str:
        """Return the type key for serialization."""
        return "formatted_output"
