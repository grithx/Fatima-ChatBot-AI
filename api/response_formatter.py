"""
ResponseFormatter - Enforces admin-selected style formatting rules
"""
import re
from typing import Tuple


class ResponseFormatter:
    """
    Formats LLM responses according to admin-selected style preferences.
    
    Supported styles:
    - "short": Short & Professional (max 2 sentences, no greetings, no marketing fluff)
    - "conversational": Human-like & Conversational (max 3 sentences, conditional greetings)
    """
    
    # Marketing fluff phrases to remove (ordered from most specific to least specific)
    FLUFF_PATTERNS = [
        # Combined patterns first
        r"As an AI(?:\s+(?:assistant|model|language model))?,?\s+I can help(?:\s+you)?(?:\s+with that)?\.?\s*",
        # Standalone patterns
        r"As an AI(?:\s+(?:assistant|model|language model))?[,\s]+",
        r"I can help(?:\s+you)?(?:\s+with that)?\.?\s*",
        r"Here (?:are|is) some[,\s]+",
        r"Based on your request[,\s]+",
        r"Let me (?:help|assist)(?:\s+you)?(?:\s+with that)?\.?\s*",
        r"I'm (?:here|glad) to (?:help|assist)(?:\s+you)?[,\s]+",
        r"As your (?:assistant|support)[,\s]+",
    ]
    
    # Greeting patterns to detect in user input
    USER_GREETING_PATTERNS = [
        r"^(?:hi|hello|hey|greetings|good\s+(?:morning|afternoon|evening|day))",
    ]
    
    # Greeting patterns in bot responses
    BOT_GREETING_PATTERNS = [
        r"^(?:Hi|Hello|Hey|Greetings|Good\s+(?:morning|afternoon|evening|day))(?:\s+there)?[,!\s]+",
    ]
    
    # Apology patterns
    APOLOGY_PATTERNS = [
        r"I (?:am )?sorry[,\s]+",
        r"I apologize[,\s]+",
        r"Apologies[,\s]+",
    ]
    
    # URL/hyperlink pattern
    URL_PATTERN = r"https?://[^\s<>\"\']+"
    
    # Pricing/policy keywords for sentence prioritization
    PRICING_KEYWORDS = ["price", "cost", "pkr", "$", "pricing", "plan", "package"]
    POLICY_KEYWORDS = ["policy", "refund", "terms", "condition", "guarantee"]
    
    def __init__(self, style: str = "short"):
        """
        Initialize ResponseFormatter with a style.
        
        Args:
            style: Either "short" or "conversational"
        """
        self.style = style.lower()
        if self.style not in ["short", "conversational"]:
            self.style = "short"  # Default to short
    
    def format(self, response: str, user_input: str = "") -> str:
        """
        Format the LLM response according to the selected style.
        
        Args:
            response: Raw LLM response
            user_input: Original user input (for greeting detection)
        
        Returns:
            Formatted response
        """
        if not response or not response.strip():
            return response
        
        # Step 1: Remove marketing fluff
        response = self._remove_marketing_fluff(response)
        
        # Step 2: Handle greetings based on style
        response = self._handle_greetings(response, user_input)
        
        # Step 3: Remove apologies if short style
        if self.style == "short":
            response = self._remove_apologies(response)
        
        # Step 4: Remove hyperlinks if not requested
        response = self._handle_hyperlinks(response, user_input)
        
        # Step 5: Prioritize pricing/policy sentences
        response = self._prioritize_key_sentences(response)
        
        # Step 6: Limit sentences based on style
        response = self._limit_sentences(response)
        
        # Step 7: Clean up extra whitespace and formatting
        response = self._clean_response(response)
        
        return response
    
    def _remove_marketing_fluff(self, text: str) -> str:
        """Remove marketing fluff phrases."""
        for pattern in self.FLUFF_PATTERNS:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)
        return text
    
    def _handle_greetings(self, response: str, user_input: str) -> str:
        """
        Handle greetings based on style and user input.
        
        - Short style: Always remove greetings
        - Conversational style: Keep greeting only if user greeted first
        """
        if self.style == "short":
            # Remove all greetings
            for pattern in self.BOT_GREETING_PATTERNS:
                response = re.sub(pattern, "", response, flags=re.IGNORECASE)
        elif self.style == "conversational":
            # Check if user greeted
            user_greeted = any(
                re.search(pattern, user_input.strip(), flags=re.IGNORECASE)
                for pattern in self.USER_GREETING_PATTERNS
            )
            
            # Remove greeting if user didn't greet
            if not user_greeted:
                for pattern in self.BOT_GREETING_PATTERNS:
                    response = re.sub(pattern, "", response, flags=re.IGNORECASE)
        
        return response
    
    def _remove_apologies(self, text: str) -> str:
        """Remove apology phrases (for short style)."""
        for pattern in self.APOLOGY_PATTERNS:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)
        return text
    
    def _handle_hyperlinks(self, text: str, user_input: str) -> str:
        """
        Remove hyperlinks unless explicitly requested.
        
        User must mention: link, url, website, site, etc.
        """
        link_keywords = ["link", "url", "website", "site", "web page"]
        user_wants_link = any(
            keyword in user_input.lower() for keyword in link_keywords
        )
        
        if not user_wants_link:
            text = re.sub(self.URL_PATTERN, "", text)
        
        return text
    
    def _prioritize_key_sentences(self, text: str) -> str:
        """
        If answer contains pricing or policy info, move it to the first sentence.
        """
        # Split into sentences
        sentences = self._split_sentences(text)
        
        if len(sentences) <= 1:
            return text
        
        # Find first sentence with pricing or policy keywords
        key_sentence_idx = None
        for i, sentence in enumerate(sentences):
            sentence_lower = sentence.lower()
            has_pricing = any(kw in sentence_lower for kw in self.PRICING_KEYWORDS)
            has_policy = any(kw in sentence_lower for kw in self.POLICY_KEYWORDS)
            
            if has_pricing or has_policy:
                key_sentence_idx = i
                break
        
        # Move key sentence to first position if found and not already first
        if key_sentence_idx and key_sentence_idx > 0:
            key_sentence = sentences.pop(key_sentence_idx)
            sentences.insert(0, key_sentence)
        
        return " ".join(sentences)
    
    def _limit_sentences(self, text: str) -> str:
        """
        Limit number of sentences based on style.
        
        - Short: max 2 sentences
        - Conversational: max 3 sentences
        """
        max_sentences = 2 if self.style == "short" else 3
        
        sentences = self._split_sentences(text)
        
        if len(sentences) <= max_sentences:
            return text
        
        # Keep only first N sentences
        limited = sentences[:max_sentences]
        return " ".join(limited)
    
    def _split_sentences(self, text: str) -> list:
        """
        Split text into sentences, handling common edge cases.
        
        Returns:
            List of sentences (stripped)
        """
        # Basic sentence splitting on . ! ?
        # Keep periods in numbers and abbreviations
        text = re.sub(r'([.!?])\s+', r'\1|SENT_BREAK|', text)
        sentences = text.split('|SENT_BREAK|')
        
        # Clean and filter empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def _clean_response(self, text: str) -> str:
        """
        Clean up the response: remove extra whitespace, fix punctuation.
        """
        # Protect URLs from cleaning by temporarily replacing them
        url_placeholders = {}
        urls = re.findall(self.URL_PATTERN, text)
        for i, url in enumerate(urls):
            placeholder = f"___URL_{i}___"
            url_placeholders[placeholder] = url
            text = text.replace(url, placeholder)
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Fix spacing around punctuation (but not for protected URLs)
        text = re.sub(r'\s+([.,!?])', r'\1', text)
        
        # Ensure single space after punctuation
        text = re.sub(r'([.,!?])([A-Za-z])', r'\1 \2', text)
        
        # Restore URLs
        for placeholder, url in url_placeholders.items():
            text = text.replace(placeholder, url)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        # Ensure ends with proper punctuation
        if text and text[-1] not in '.!?':
            text += '.'
        
        return text
