"""
Unit tests for FormattedOutputParser
"""
import unittest
import sys
sys.path.insert(0, 'api')

from output_parser import FormattedOutputParser


class TestFormattedOutputParser(unittest.TestCase):
    """Test cases for FormattedOutputParser class"""
    
    def test_parse_returns_structured_output(self):
        """Test that parse returns dictionary with expected keys"""
        parser = FormattedOutputParser(style="short")
        result = parser.parse("Our VPS plans start at PKR 3000.")
        
        self.assertIn("final_text", result)
        self.assertIn("tokens_used", result)
        self.assertIn("truncated", result)
        self.assertIsInstance(result["tokens_used"], int)
        self.assertIsInstance(result["truncated"], bool)
    
    def test_empty_response_returns_fallback(self):
        """Test that empty response returns clarification question"""
        parser = FormattedOutputParser(style="short")
        result = parser.parse("")
        
        self.assertIn("rephrase", result["final_text"].lower())
        self.assertFalse(result["truncated"])
        self.assertGreater(result["tokens_used"], 0)
    
    def test_whitespace_only_returns_fallback(self):
        """Test that whitespace-only response returns fallback"""
        parser = FormattedOutputParser(style="short")
        result = parser.parse("   \n\n   ")
        
        self.assertIn("rephrase", result["final_text"].lower())
    
    def test_code_fences_removed_by_default(self):
        """Test that code fences are removed when not requested"""
        parser = FormattedOutputParser(style="short", user_input="What is pricing?")
        text = "Our plans cost PKR 2000. ```python\nprint('hello')\n``` Contact us for details."
        result = parser.parse(text)
        
        self.assertNotIn("```", result["final_text"])
        self.assertNotIn("python", result["final_text"])
        self.assertNotIn("print", result["final_text"])
    
    def test_code_fences_kept_when_requested(self):
        """Test that code fences are kept when user asks for code"""
        parser = FormattedOutputParser(style="short", user_input="Show me code example")
        text = "Here's an example: ```python\nprint('hello')\n```"
        result = parser.parse(text)
        
        # Code should be kept (though formatting may change)
        self.assertIn("example", result["final_text"])
    
    def test_inline_code_removed(self):
        """Test that inline code backticks are removed"""
        parser = FormattedOutputParser(style="short", user_input="pricing?")
        text = "Use the `cPanel` interface. Plans cost `PKR 2000`."
        result = parser.parse(text)
        
        self.assertNotIn("`", result["final_text"])
        self.assertIn("cPanel", result["final_text"])
        self.assertIn("PKR", result["final_text"])
    
    def test_unhelpful_response_returns_clarification(self):
        """Test that unhelpful responses trigger fallback"""
        parser = FormattedOutputParser(style="short")
        
        unhelpful_texts = [
            "I don't know.",
            "I don't have that information.",
            "I can't help with that.",
            "Sorry, I'm not sure."
        ]
        
        for text in unhelpful_texts:
            result = parser.parse(text)
            self.assertIn("more details", result["final_text"].lower())
    
    def test_truncated_flag_set_when_shortened(self):
        """Test that truncated flag is set when response is shortened"""
        parser = FormattedOutputParser(style="short")
        # Long response that will be truncated to 2 sentences
        text = "First sentence. Second sentence. Third sentence. Fourth sentence. Fifth sentence."
        result = parser.parse(text)
        
        # Should be truncated since short style allows max 2 sentences
        # and we had 5 sentences
        self.assertTrue(result["truncated"])
    
    def test_truncated_flag_false_when_not_shortened(self):
        """Test that truncated flag is False when response fits"""
        parser = FormattedOutputParser(style="short")
        text = "Our plans start at PKR 2000."
        result = parser.parse(text)
        
        # Single sentence, no truncation needed
        self.assertFalse(result["truncated"])
    
    def test_token_estimation(self):
        """Test that token count is estimated reasonably"""
        parser = FormattedOutputParser(style="short")
        text = "Our VPS hosting plans start at PKR 3000 per month."
        result = parser.parse(text)
        
        # 10 words * 1.3 = ~13 tokens
        self.assertGreater(result["tokens_used"], 10)
        self.assertLess(result["tokens_used"], 20)
    
    def test_short_style_formatting(self):
        """Test that short style formatting is applied"""
        parser = FormattedOutputParser(style="short", user_input="pricing?")
        text = "Hello! As an AI, I can help. Our VPS plans cost PKR 3000. We provide support. Backups included."
        result = parser.parse(text)
        
        # Should remove greeting and limit sentences
        self.assertNotIn("Hello", result["final_text"])
        self.assertNotIn("As an AI", result["final_text"])
        
        # Count sentences (approximately)
        sentences = [s for s in result["final_text"].split('.') if s.strip()]
        self.assertLessEqual(len(sentences), 2)
    
    def test_conversational_style_with_greeting(self):
        """Test conversational style keeps greeting when user greets"""
        parser = FormattedOutputParser(style="conversational", user_input="Hi! What are your prices?")
        text = "Hello! Our plans start at PKR 2000. We offer great service. Support is 24/7."
        result = parser.parse(text)
        
        # Should keep greeting since user greeted
        self.assertIn("Hello", result["final_text"])
    
    def test_conversational_style_without_greeting(self):
        """Test conversational style removes greeting when user doesn't greet"""
        parser = FormattedOutputParser(style="conversational", user_input="What are your prices?")
        text = "Hello! Our plans start at PKR 2000. We offer great service."
        result = parser.parse(text)
        
        # Should remove greeting since user didn't greet
        self.assertNotIn("Hello", result["final_text"])
    
    def test_conversational_allows_three_sentences(self):
        """Test that conversational style allows up to 3 sentences"""
        parser = FormattedOutputParser(style="conversational")
        text = "First. Second. Third. Fourth. Fifth."
        result = parser.parse(text)
        
        sentences = [s for s in result["final_text"].split('.') if s.strip()]
        self.assertLessEqual(len(sentences), 3)
    
    def test_useful_response_with_dont_know_phrase(self):
        """Test that longer responses with 'don't know' are still considered useful"""
        parser = FormattedOutputParser(style="short")
        text = "I don't know the exact price off-hand, but our VPS hosting typically starts around PKR 3000 per month. You can check our pricing page for current rates."
        result = parser.parse(text)
        
        # Should not trigger fallback because response is long enough
        self.assertNotIn("more details", result["final_text"].lower())
        self.assertIn("VPS", result["final_text"])
    
    def test_sentence_counting(self):
        """Test sentence counting logic"""
        parser = FormattedOutputParser(style="short")
        
        # Test various sentence structures
        self.assertEqual(parser._count_sentences("One."), 1)
        self.assertEqual(parser._count_sentences("One. Two."), 2)
        self.assertEqual(parser._count_sentences("One! Two? Three."), 3)
        self.assertEqual(parser._count_sentences("Hello! How are you?"), 2)
    
    def test_user_wants_code_detection(self):
        """Test detection of code-related requests"""
        # Should detect code requests
        parser1 = FormattedOutputParser(user_input="show me a code example")
        self.assertTrue(parser1._user_wants_code())
        
        parser2 = FormattedOutputParser(user_input="what's the command to install?")
        self.assertTrue(parser2._user_wants_code())
        
        # Should not detect as code request
        parser3 = FormattedOutputParser(user_input="what are your pricing plans?")
        self.assertFalse(parser3._user_wants_code())
    
    def test_metadata_source_not_in_llm_response(self):
        """Test that LLM responses don't include 'source' in metadata"""
        parser = FormattedOutputParser(style="short")
        result = parser.parse("Our plans cost PKR 2000.")
        
        # Standard parse should not include 'source' key
        # (source is added by app.py for database responses)
        self.assertNotIn("source", result)
    
    def test_multiple_code_blocks(self):
        """Test removal of multiple code blocks"""
        parser = FormattedOutputParser(style="short", user_input="pricing?")
        text = "First block: ```bash\nls -la\n``` and second: ```python\nprint()\n``` Our plans cost PKR 2000."
        result = parser.parse(text)
        
        self.assertNotIn("```", result["final_text"])
        self.assertNotIn("bash", result["final_text"])
        self.assertNotIn("python", result["final_text"])


if __name__ == '__main__':
    unittest.main()
