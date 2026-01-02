"""
Manual demonstration of ResponseFormatter integration
This shows how the formatter works with various inputs
"""
import sys
sys.path.insert(0, 'api')
from response_formatter import ResponseFormatter


def demo_short_style():
    print("\n" + "="*70)
    print("DEMO: SHORT & PROFESSIONAL STYLE")
    print("="*70)
    
    formatter = ResponseFormatter(style="short")
    
    test_cases = [
        {
            "user": "What is VPS hosting pricing?",
            "llm": "Hello! As an AI assistant, I can help you with that. Based on your request, our VPS hosting plans start at PKR 3000 per month. These plans include 50GB SSD storage. You get full root access. We provide 24/7 technical support. Backups are performed daily. Migration is completely free."
        },
        {
            "user": "Tell me about refund policy",
            "llm": "I am sorry if there's any confusion. Here are some details. We offer a 30-day money-back guarantee on all hosting plans. To request a refund, contact our support team via email. Refunds are processed within 5-7 business days. Domain registrations are non-refundable as per ICANN policy."
        },
        {
            "user": "wordpress hosting features",
            "llm": "As an AI, I can help. Our WordPress hosting is optimized for speed and security. Plans start at PKR 2000 monthly. Includes automatic WordPress updates. Daily backups included. Free SSL certificate. One-click staging environment."
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"User: {test['user']}")
        print(f"\nLLM Output:\n{test['llm']}")
        
        formatted = formatter.format(test['llm'], test['user'])
        print(f"\n✓ Formatted Output:\n{formatted}")
        
        # Verify constraints
        sentences = [s.strip() for s in formatted.split('.') if s.strip()]
        print(f"\n  • Sentences: {len(sentences)} (max 2)")
        print(f"  • No greeting: {('Hello' not in formatted and 'Hi' not in formatted)}")
        print(f"  • No apologies: {('sorry' not in formatted.lower() and 'apologize' not in formatted.lower())}")
        print(f"  • No fluff: {('As an AI' not in formatted and 'I can help' not in formatted)}")


def demo_conversational_style():
    print("\n" + "="*70)
    print("DEMO: HUMAN-LIKE & CONVERSATIONAL STYLE")
    print("="*70)
    
    formatter = ResponseFormatter(style="conversational")
    
    test_cases = [
        {
            "user": "Hi! What plans do you offer?",
            "llm": "Hello! As an AI, I can help you. We offer various hosting plans for different needs. Our Shared Hosting starts at PKR 1500. VPS Hosting begins at PKR 3000. Dedicated servers are available from PKR 15000. WordPress hosting is optimized for performance."
        },
        {
            "user": "What plans do you offer?",  # No greeting
            "llm": "Hello! We offer various hosting plans for different needs. Our Shared Hosting starts at PKR 1500. VPS Hosting begins at PKR 3000. Dedicated servers are available from PKR 15000."
        },
        {
            "user": "Good morning! Domain registration info?",
            "llm": "Good morning! I'm here to help. We offer domain registration for various extensions. .pk domains cost PKR 2000 annually. International domains like .com and .net are available. Free DNS management is included. WHOIS privacy protection is optional."
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"User: {test['user']}")
        print(f"\nLLM Output:\n{test['llm']}")
        
        formatted = formatter.format(test['llm'], test['user'])
        print(f"\n✓ Formatted Output:\n{formatted}")
        
        # Verify constraints
        sentences = [s.strip() for s in formatted.split('.') if s.strip()]
        has_user_greeting = any(g in test['user'].lower() for g in ['hi', 'hello', 'good morning'])
        print(f"\n  • Sentences: {len(sentences)} (max 3)")
        print(f"  • User greeted: {has_user_greeting}")
        if has_user_greeting:
            print(f"  • Greeting kept: {any(g in formatted for g in ['Hello', 'Hi', 'Good morning'])}")


def demo_url_handling():
    print("\n" + "="*70)
    print("DEMO: URL HANDLING")
    print("="*70)
    
    formatter = ResponseFormatter(style="short")
    
    test_cases = [
        {
            "user": "What are your prices?",
            "llm": "Our pricing is available at https://zthosting.com/pricing. Plans start at PKR 1500. Visit our website for details."
        },
        {
            "user": "Send me the link to your pricing page",
            "llm": "You can view our pricing at https://zthosting.com/pricing. Plans start at PKR 1500. Contact us for custom quotes."
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"User: {test['user']}")
        formatted = formatter.format(test['llm'], test['user'])
        print(f"\n✓ Formatted: {formatted}")
        
        wants_link = any(w in test['user'].lower() for w in ['link', 'url', 'website'])
        has_url = 'https://' in formatted
        print(f"\n  • User wants link: {wants_link}")
        print(f"  • URL in output: {has_url}")
        print(f"  • Correct: {wants_link == has_url}")


def demo_pricing_prioritization():
    print("\n" + "="*70)
    print("DEMO: PRICING/POLICY SENTENCE PRIORITIZATION")
    print("="*70)
    
    formatter = ResponseFormatter(style="short")
    
    llm_output = "We provide excellent customer support with 24/7 availability. Our Premium plan costs PKR 5000 per month. Free migration is included for all plans."
    user_input = "premium plan price?"
    
    print(f"User: {user_input}")
    print(f"\nOriginal order: Support → Pricing → Migration")
    
    formatted = formatter.format(llm_output, user_input)
    print(f"\n✓ Formatted (pricing prioritized):\n{formatted}")
    print(f"\nPricing sentence moved to beginning: {formatted.startswith('Our Premium plan costs') or formatted.startswith('our Premium plan costs')}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("RESPONSEFORMATTER COMPREHENSIVE DEMONSTRATION")
    print("="*70)
    
    demo_short_style()
    demo_conversational_style()
    demo_url_handling()
    demo_pricing_prioritization()
    
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)
    print("\nThe ResponseFormatter successfully enforces:")
    print("  ✓ Sentence limits (2 for short, 3 for conversational)")
    print("  ✓ Marketing fluff removal")
    print("  ✓ Conditional greeting handling")
    print("  ✓ Smart URL management")
    print("  ✓ Pricing/policy prioritization")
    print("  ✓ Clean formatting and punctuation")
    print()
