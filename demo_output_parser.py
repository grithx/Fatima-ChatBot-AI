"""
Demonstration of FormattedOutputParser with structured output
Shows the new LangChain integration features
"""
import sys
sys.path.insert(0, 'api')

from output_parser import FormattedOutputParser


def demo_structured_output():
    print("\n" + "="*70)
    print("DEMO: STRUCTURED OUTPUT WITH METADATA")
    print("="*70)
    
    parser = FormattedOutputParser(style="short", user_input="What are VPS prices?")
    
    llm_output = """Hello! As an AI assistant, I can help you with that. 
    Our VPS hosting plans start at PKR 3000 per month. 
    These plans include 50GB SSD storage. 
    You get full root access. 
    We provide 24/7 technical support. 
    Backups are performed daily."""
    
    result = parser.parse(llm_output)
    
    print("\nLLM Output (raw):")
    print(llm_output.strip())
    print("\n" + "-"*70)
    print("\nStructured Result:")
    print(f"  final_text: {result['final_text']}")
    print(f"  tokens_used: {result['tokens_used']}")
    print(f"  truncated: {result['truncated']}")
    print("\n✓ Returns structured dictionary with metadata")


def demo_code_fence_removal():
    print("\n" + "="*70)
    print("DEMO: CODE FENCE REMOVAL")
    print("="*70)
    
    # Case 1: Remove code when not requested
    parser1 = FormattedOutputParser(style="short", user_input="pricing info")
    llm_with_code = """Our plans cost PKR 2000 per month. 
    Here's a sample config:
    ```bash
    apt-get install package
    systemctl start service
    ```
    Contact our support team for assistance."""
    
    result1 = parser1.parse(llm_with_code)
    
    print("\n--- Case 1: User didn't ask for code ---")
    print("User input: 'pricing info'")
    print("\nLLM output includes code block:")
    print(llm_with_code.strip()[:200] + "...")
    print("\nFormatted output (code removed):")
    print(f"  {result1['final_text']}")
    print(f"  Contains code fences: {'```' in result1['final_text']}")
    
    # Case 2: Keep code when requested
    parser2 = FormattedOutputParser(style="short", user_input="show me the command")
    result2 = parser2.parse(llm_with_code)
    
    print("\n--- Case 2: User asked for code ---")
    print("User input: 'show me the command'")
    print("\nFormatted output (code kept):")
    print(f"  {result2['final_text'][:100]}...")
    print(f"  Code preserved: {parser2._user_wants_code()}")


def demo_fallback_handling():
    print("\n" + "="*70)
    print("DEMO: FALLBACK HANDLING")
    print("="*70)
    
    parser = FormattedOutputParser(style="short")
    
    # Case 1: Empty response
    result1 = parser.parse("")
    print("\n--- Case 1: Empty LLM Response ---")
    print("LLM output: (empty)")
    print(f"Fallback: {result1['final_text']}")
    
    # Case 2: Unhelpful response
    result2 = parser.parse("I don't know.")
    print("\n--- Case 2: Unhelpful Response ---")
    print("LLM output: 'I don't know.'")
    print(f"Fallback: {result2['final_text']}")
    
    # Case 3: Useful response with "don't know" phrase
    result3 = parser.parse("I don't know the exact figure, but VPS hosting typically costs around PKR 3000 per month. Check our pricing page for current rates.")
    print("\n--- Case 3: Useful Response (no fallback) ---")
    print("LLM output includes 'don't know' but is detailed enough")
    print(f"Output: {result3['final_text']}")
    print(f"Fallback triggered: {len(result3['final_text']) < 50}")


def demo_token_tracking():
    print("\n" + "="*70)
    print("DEMO: TOKEN USAGE TRACKING")
    print("="*70)
    
    test_cases = [
        ("Short response", "Our plans cost PKR 2000."),
        ("Medium response", "Our VPS plans start at PKR 3000 per month. They include 50GB storage and 24/7 support."),
        ("Long response", "Hello! Our VPS hosting is perfect for developers. Plans start at PKR 3000. Storage is 50GB SSD. Bandwidth is unlimited. Support is 24/7. Backups are daily.")
    ]
    
    for name, text in test_cases:
        parser = FormattedOutputParser(style="short")
        result = parser.parse(text)
        
        words = len(result['final_text'].split())
        print(f"\n{name}:")
        print(f"  Words: {words}")
        print(f"  Tokens (estimated): {result['tokens_used']}")
        print(f"  Ratio: ~{result['tokens_used']/words:.1f}x")


def demo_truncation_flag():
    print("\n" + "="*70)
    print("DEMO: TRUNCATION FLAG")
    print("="*70)
    
    # Case 1: No truncation needed
    parser1 = FormattedOutputParser(style="short")
    result1 = parser1.parse("Our plans cost PKR 2000.")
    
    print("\n--- Case 1: No Truncation ---")
    print("Input: 1 sentence")
    print(f"Output: {result1['final_text']}")
    print(f"Truncated: {result1['truncated']}")
    
    # Case 2: Truncation applied
    parser2 = FormattedOutputParser(style="short")
    long_text = "First sentence. Second sentence. Third sentence. Fourth sentence. Fifth sentence."
    result2 = parser2.parse(long_text)
    
    print("\n--- Case 2: Truncation Applied ---")
    print("Input: 5 sentences")
    print(f"Output: {result2['final_text']}")
    print(f"Truncated: {result2['truncated']}")


def demo_chain_integration():
    print("\n" + "="*70)
    print("DEMO: CHAIN INTEGRATION (Conceptual)")
    print("="*70)
    
    print("""
In app.py, the OutputParser is wired into a LangChain RunnableSequence:

    # Create the parser
    output_parser = FormattedOutputParser(
        style=response_style, 
        user_input=user_input
    )
    
    # Wire into chain via pipe operator
    chain = prompt | llm | output_parser
    
    # Invoke returns structured output
    result = chain.invoke({"input": user_input})
    
    # Access structured response
    {
        "answer": result["final_text"],
        "metadata": {
            "tokens_used": result["tokens_used"],
            "truncated": result["truncated"]
        }
    }

This creates a clean pipeline:
  User Input → Prompt → LLM → OutputParser → Structured Response
  
The parser automatically:
  ✓ Removes marketing fluff
  ✓ Limits sentences
  ✓ Removes code fences (unless requested)
  ✓ Provides fallbacks for empty/unhelpful responses
  ✓ Tracks tokens and truncation
    """)


if __name__ == "__main__":
    print("\n" + "="*70)
    print("FORMATTEDOUTPUTPARSER COMPREHENSIVE DEMONSTRATION")
    print("="*70)
    
    demo_structured_output()
    demo_code_fence_removal()
    demo_fallback_handling()
    demo_token_tracking()
    demo_truncation_flag()
    demo_chain_integration()
    
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)
    print("\nThe FormattedOutputParser provides:")
    print("  ✓ Structured output with metadata")
    print("  ✓ Code fence removal (unless requested)")
    print("  ✓ Intelligent fallback handling")
    print("  ✓ Token usage tracking")
    print("  ✓ Truncation detection")
    print("  ✓ Clean LangChain integration via RunnableSequence")
    print()
