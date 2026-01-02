"""
Unit tests for ResponseFormatter
"""
import unittest
from api.response_formatter import ResponseFormatter


class TestResponseFormatter(unittest.TestCase):
    """Test cases for ResponseFormatter class"""
    
    def test_init_default_style(self):
        """Test default initialization to 'short' style"""
        formatter = ResponseFormatter()
        self.assertEqual(formatter.style, "short")
    
    def test_init_short_style(self):
        """Test initialization with 'short' style"""
        formatter = ResponseFormatter(style="short")
        self.assertEqual(formatter.style, "short")
    
    def test_init_conversational_style(self):
        """Test initialization with 'conversational' style"""
        formatter = ResponseFormatter(style="conversational")
        self.assertEqual(formatter.style, "conversational")
    
    def test_init_invalid_style_defaults_to_short(self):
        """Test that invalid style defaults to 'short'"""
        formatter = ResponseFormatter(style="invalid")
        self.assertEqual(formatter.style, "short")
    
    def test_remove_marketing_fluff_as_an_ai(self):
        """Test removal of 'As an AI' fluff"""
        formatter = ResponseFormatter(style="short")
        response = "As an AI assistant, I can tell you that our VPS plans start at $10."
        result = formatter.format(response)
        self.assertNotIn("As an AI", result)
        self.assertIn("VPS plans", result)
    
    def test_remove_marketing_fluff_i_can_help(self):
        """Test removal of 'I can help' fluff"""
        formatter = ResponseFormatter(style="short")
        response = "I can help you with that. Our plans include unlimited bandwidth."
        result = formatter.format(response)
        self.assertNotIn("I can help", result)
        self.assertIn("plans include", result)
    
    def test_remove_marketing_fluff_here_are_some(self):
        """Test removal of 'Here are some' fluff"""
        formatter = ResponseFormatter(style="short")
        response = "Here are some options for you. We offer three packages."
        result = formatter.format(response)
        self.assertNotIn("Here are some", result)
        self.assertIn("offer three packages", result)
    
    def test_remove_marketing_fluff_based_on_your_request(self):
        """Test removal of 'based on your request' fluff"""
        formatter = ResponseFormatter(style="short")
        response = "Based on your request, our premium plan costs $50."
        result = formatter.format(response)
        self.assertNotIn("Based on your request", result)
        self.assertIn("premium plan", result)
    
    def test_short_style_removes_greetings(self):
        """Test that short style removes all greetings"""
        formatter = ResponseFormatter(style="short")
        response = "Hello! Our VPS hosting starts at $20. We provide 24/7 support."
        result = formatter.format(response, user_input="What is VPS pricing?")
        self.assertNotIn("Hello", result)
        self.assertIn("VPS hosting", result)
    
    def test_short_style_removes_apologies(self):
        """Test that short style removes apologies"""
        formatter = ResponseFormatter(style="short")
        response = "I am sorry, but we don't offer monthly plans. All plans are annual."
        result = formatter.format(response)
        self.assertNotIn("sorry", result.lower())
        self.assertIn("don't offer monthly plans", result)
    
    def test_conversational_keeps_greeting_when_user_greets(self):
        """Test that conversational style keeps greeting if user greeted first"""
        formatter = ResponseFormatter(style="conversational")
        response = "Hello! Our basic plan costs $10 per month. It includes 10GB storage. We also provide email support."
        result = formatter.format(response, user_input="Hi, what are your prices?")
        self.assertIn("Hello", result)
    
    def test_conversational_removes_greeting_when_user_doesnt_greet(self):
        """Test that conversational style removes greeting if user didn't greet"""
        formatter = ResponseFormatter(style="conversational")
        response = "Hello! Our basic plan costs $10 per month. It includes 10GB storage."
        result = formatter.format(response, user_input="What are your prices?")
        self.assertNotIn("Hello", result)
    
    def test_short_style_limits_to_two_sentences(self):
        """Test that short style limits response to 2 sentences"""
        formatter = ResponseFormatter(style="short")
        response = "Our VPS plans start at $20. We offer 24/7 support. Plans include SSD storage. Backups are automatic. Migration is free."
        result = formatter.format(response)
        sentences = [s.strip() for s in result.split('.') if s.strip()]
        self.assertLessEqual(len(sentences), 2)
    
    def test_conversational_style_limits_to_three_sentences(self):
        """Test that conversational style limits response to 3 sentences"""
        formatter = ResponseFormatter(style="conversational")
        response = "Our VPS plans start at $20. We offer 24/7 support. Plans include SSD storage. Backups are automatic. Migration is free."
        result = formatter.format(response)
        sentences = [s.strip() for s in result.split('.') if s.strip()]
        self.assertLessEqual(len(sentences), 3)
    
    def test_removes_hyperlinks_when_not_requested(self):
        """Test that hyperlinks are removed when not requested"""
        formatter = ResponseFormatter(style="short")
        response = "Visit our site at https://example.com for more details. Our plans start at $10."
        result = formatter.format(response, user_input="What are your prices?")
        self.assertNotIn("https://", result)
        self.assertIn("plans start", result)
    
    def test_keeps_hyperlinks_when_requested(self):
        """Test that hyperlinks are kept when user requests them"""
        formatter = ResponseFormatter(style="short")
        response = "Visit our site at https://example.com for more details. Our plans start at $10."
        result = formatter.format(response, user_input="Can you give me the link to your website?")
        self.assertIn("https://example.com", result)
    
    def test_prioritizes_pricing_sentence(self):
        """Test that sentences with pricing keywords are prioritized"""
        formatter = ResponseFormatter(style="short")
        response = "We offer 24/7 support. Our VPS plans cost $20 per month. Migration is included."
        result = formatter.format(response)
        # The pricing sentence should come first
        self.assertTrue(result.startswith("Our VPS plans cost"))
    
    def test_prioritizes_policy_sentence(self):
        """Test that sentences with policy keywords are prioritized"""
        formatter = ResponseFormatter(style="short")
        response = "We provide excellent service. Our refund policy allows 30 days. Support is 24/7."
        result = formatter.format(response)
        # The policy sentence should come first
        self.assertTrue(result.startswith("Our refund policy"))
    
    def test_cleans_extra_whitespace(self):
        """Test that extra whitespace is cleaned up"""
        formatter = ResponseFormatter(style="short")
        response = "Our plans    include   unlimited   bandwidth.   24/7  support  available."
        result = formatter.format(response)
        self.assertNotIn("  ", result)  # No double spaces
    
    def test_adds_period_if_missing(self):
        """Test that a period is added if response doesn't end with punctuation"""
        formatter = ResponseFormatter(style="short")
        response = "Our VPS plans start at $20"
        result = formatter.format(response)
        self.assertTrue(result.endswith('.') or result.endswith('!') or result.endswith('?'))
    
    def test_handles_empty_response(self):
        """Test handling of empty responses"""
        formatter = ResponseFormatter(style="short")
        result = formatter.format("")
        self.assertEqual(result, "")
    
    def test_handles_whitespace_only_response(self):
        """Test handling of whitespace-only responses"""
        formatter = ResponseFormatter(style="short")
        result = formatter.format("   ")
        self.assertEqual(result, "   ")
    
    def test_complex_response_short_style(self):
        """Test complex response with short style"""
        formatter = ResponseFormatter(style="short")
        response = "Hello! As an AI assistant, I can help you. Here are some details. Based on your request, our Premium plan costs PKR 5000 per month. It includes 100GB SSD storage. You get unlimited bandwidth. We provide 24/7 support. Visit https://example.com for more info."
        result = formatter.format(response, user_input="What is the premium plan price?")
        
        # Should not have marketing fluff
        self.assertNotIn("As an AI", result)
        self.assertNotIn("I can help", result)
        self.assertNotIn("Here are some", result)
        self.assertNotIn("Based on your request", result)
        
        # Should not have greetings
        self.assertNotIn("Hello", result)
        
        # Should not have hyperlinks
        self.assertNotIn("https://", result)
        
        # Should have pricing info prioritized and be max 2 sentences
        sentences = [s.strip() for s in result.split('.') if s.strip()]
        self.assertLessEqual(len(sentences), 2)
        self.assertIn("PKR 5000", result)
    
    def test_complex_response_conversational_style_with_greeting(self):
        """Test complex response with conversational style when user greets"""
        formatter = ResponseFormatter(style="conversational")
        response = "Hello! As an AI, I can help you with that. Based on your request, our Basic plan costs $10. It includes 10GB storage. We offer email support. Backups are weekly. Migration is included."
        result = formatter.format(response, user_input="Hi! What are your basic plans?")
        
        # Should keep greeting since user greeted
        self.assertIn("Hello", result)
        
        # Should not have marketing fluff
        self.assertNotIn("As an AI", result)
        
        # Should be max 3 sentences
        sentences = [s.strip() for s in result.split('.') if s.strip()]
        self.assertLessEqual(len(sentences), 3)
    
    def test_bold_formatting_preserved(self):
        """Test that bold markdown formatting is preserved"""
        formatter = ResponseFormatter(style="short")
        response = "Our Premium plan costs **PKR 5000**. It includes **unlimited bandwidth**."
        result = formatter.format(response)
        self.assertIn("**PKR 5000**", result)
        self.assertIn("**unlimited bandwidth**", result)
    
    def test_sentence_with_multiple_periods(self):
        """Test handling of sentences with abbreviations containing periods"""
        formatter = ResponseFormatter(style="short")
        response = "Contact us at support@example.com for details. We offer U.S. based support. Plans start at $10."
        result = formatter.format(response)
        # Should still respect sentence limits (approximately)
        # Note: This is a complex case with emails and abbreviations
        sentences = [s.strip() for s in result.split('.') if s.strip()]
        # Allow some flexibility for complex punctuation
        self.assertLessEqual(len(sentences), 3)


if __name__ == '__main__':
    unittest.main()
