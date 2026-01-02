"""
Integration test for ResponseFormatter with the API endpoint.
This tests the full flow without requiring actual API keys.
"""
import sys
sys.path.insert(0, 'api')

from response_formatter import ResponseFormatter


def test_short_style_integration():
    """Test short style formatting in an integration scenario"""
    # Simulate what would come from LLM
    llm_response = (
        "Hello! As an AI assistant, I can help you with that. "
        "Based on your request, our Premium VPS plan costs PKR 5000 per month. "
        "It includes 100GB SSD storage. You get unlimited bandwidth. "
        "We provide 24/7 support with live chat. "
        "Visit https://example.com/vps for more details."
    )
    
    user_input = "What is the premium VPS pricing?"
    
    formatter = ResponseFormatter(style="short")
    result = formatter.format(llm_response, user_input)
    
    print("=" * 60)
    print("SHORT STYLE TEST")
    print("=" * 60)
    print(f"User: {user_input}")
    print(f"\nLLM Response:\n{llm_response}")
    print(f"\nFormatted Response:\n{result}")
    print("=" * 60)
    
    # Verify formatting rules
    assert "Hello" not in result, "Should not contain greeting"
    assert "As an AI" not in result, "Should not contain marketing fluff"
    assert "Based on your request" not in result, "Should not contain marketing fluff"
    assert "https://" not in result, "Should not contain URLs (not requested)"
    assert "PKR 5000" in result, "Should contain pricing info"
    
    # Count sentences
    sentences = [s.strip() for s in result.split('.') if s.strip()]
    assert len(sentences) <= 2, f"Should have max 2 sentences, got {len(sentences)}"
    
    # Pricing should be first
    assert result.startswith("our Premium VPS plan costs") or result.startswith("Our Premium VPS plan costs"), \
        "Pricing sentence should be first"
    
    print("✓ All short style assertions passed!\n")


def test_conversational_style_with_greeting():
    """Test conversational style when user greets"""
    llm_response = (
        "Hello! As an AI, I can help. "
        "Our Shared Hosting plans are perfect for beginners. "
        "The Basic plan costs PKR 1500 per month. "
        "It includes 20GB storage and unlimited bandwidth. "
        "We provide email support and one-click installers. "
        "Migration assistance is also available."
    )
    
    user_input = "Hi! What are your shared hosting options?"
    
    formatter = ResponseFormatter(style="conversational")
    result = formatter.format(llm_response, user_input)
    
    print("=" * 60)
    print("CONVERSATIONAL STYLE TEST (with greeting)")
    print("=" * 60)
    print(f"User: {user_input}")
    print(f"\nLLM Response:\n{llm_response}")
    print(f"\nFormatted Response:\n{result}")
    print("=" * 60)
    
    # Should keep greeting since user greeted
    assert "Hello" in result, "Should contain greeting when user greets"
    
    # Should remove marketing fluff
    assert "As an AI" not in result, "Should not contain marketing fluff"
    
    # Count sentences
    sentences = [s.strip() for s in result.split('.') if s.strip()]
    assert len(sentences) <= 3, f"Should have max 3 sentences, got {len(sentences)}"
    
    print("✓ All conversational style assertions passed!\n")


def test_conversational_style_without_greeting():
    """Test conversational style when user doesn't greet"""
    llm_response = (
        "Hello! Our WordPress hosting is optimized for speed. "
        "Plans start at PKR 2000 per month. "
        "Includes automatic updates and daily backups."
    )
    
    user_input = "WordPress hosting pricing?"
    
    formatter = ResponseFormatter(style="conversational")
    result = formatter.format(llm_response, user_input)
    
    print("=" * 60)
    print("CONVERSATIONAL STYLE TEST (without greeting)")
    print("=" * 60)
    print(f"User: {user_input}")
    print(f"\nLLM Response:\n{llm_response}")
    print(f"\nFormatted Response:\n{result}")
    print("=" * 60)
    
    # Should remove greeting since user didn't greet
    assert "Hello" not in result, "Should not contain greeting when user doesn't greet"
    
    # Count sentences
    sentences = [s.strip() for s in result.split('.') if s.strip()]
    assert len(sentences) <= 3, f"Should have max 3 sentences, got {len(sentences)}"
    
    print("✓ All conversational (no greeting) assertions passed!\n")


def test_url_handling():
    """Test that URLs are kept when requested"""
    llm_response = (
        "You can find more details on our website at https://zthosting.com/plans. "
        "Our support email is support@zthosting.com. "
        "Plans start at PKR 1000 per month."
    )
    
    user_input = "Can you send me the link to your plans?"
    
    formatter = ResponseFormatter(style="short")
    result = formatter.format(llm_response, user_input)
    
    print("=" * 60)
    print("URL HANDLING TEST")
    print("=" * 60)
    print(f"User: {user_input}")
    print(f"\nLLM Response:\n{llm_response}")
    print(f"\nFormatted Response:\n{result}")
    print("=" * 60)
    
    # Should keep URL since user asked for link
    assert "https://zthosting.com/plans" in result, "Should keep URL when requested"
    
    print("✓ URL handling assertions passed!\n")


def test_database_faq_formatting():
    """Test formatting of database FAQ responses"""
    # Simulate a database FAQ response
    db_response = (
        "Hello! I apologize for any confusion. "
        "Here are some details about our refund policy. "
        "We offer a 30-day money-back guarantee on all hosting plans. "
        "To request a refund, simply contact our support team. "
        "Refunds are processed within 5-7 business days. "
        "Domain registrations are non-refundable."
    )
    
    user_input = "What is your refund policy?"
    
    formatter = ResponseFormatter(style="short")
    result = formatter.format(db_response, user_input)
    
    print("=" * 60)
    print("DATABASE FAQ FORMATTING TEST")
    print("=" * 60)
    print(f"User: {user_input}")
    print(f"\nDatabase FAQ Response:\n{db_response}")
    print(f"\nFormatted Response:\n{result}")
    print("=" * 60)
    
    # Should remove greetings and apologies
    assert "Hello" not in result, "Should not contain greeting"
    assert "apologize" not in result and "sorry" not in result.lower(), "Should not contain apologies"
    
    # Should remove fluff
    assert "Here are some" not in result, "Should not contain marketing fluff"
    
    # Should prioritize policy sentence
    assert "30-day money-back guarantee" in result, "Should contain policy info"
    
    # Count sentences
    sentences = [s.strip() for s in result.split('.') if s.strip()]
    assert len(sentences) <= 2, f"Should have max 2 sentences, got {len(sentences)}"
    
    print("✓ Database FAQ formatting assertions passed!\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("RUNNING INTEGRATION TESTS FOR RESPONSEFORMATTER")
    print("=" * 60 + "\n")
    
    try:
        test_short_style_integration()
        test_conversational_style_with_greeting()
        test_conversational_style_without_greeting()
        test_url_handling()
        test_database_faq_formatting()
        
        print("\n" + "=" * 60)
        print("✓ ALL INTEGRATION TESTS PASSED!")
        print("=" * 60 + "\n")
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")
        sys.exit(1)
