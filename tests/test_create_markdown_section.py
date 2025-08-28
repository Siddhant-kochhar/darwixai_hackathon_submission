#!/usr/bin/env python3
"""
Test script for the create_markdown_section function
"""

from empathetic_code_reviewer import create_markdown_section


def test_create_markdown_section():
    """
    Test the create_markdown_section function with various AI responses.
    """
    print("Testing create_markdown_section function...\n")
    
    # Test cases with different AI response formats
    test_cases = [
        {
            "name": "Well-structured AI response",
            "original_comment": "Don't use hardcoded 3.14, use math.pi instead",
            "ai_response": """Great effort on implementing the area calculation! Here's an opportunity to enhance the precision and follow Python conventions.

This helps improve accuracy because math.pi provides higher precision than the hardcoded 3.14, which is crucial for mathematical calculations.

Here's the improved version:

```python
import math

def calculate_area(radius):
    return math.pi * radius * radius
```

This change makes your code more precise and follows Python best practices!"""
        },
        {
            "name": "Simple AI response",
            "original_comment": "Missing input validation",
            "ai_response": """Consider adding input validation to make your function more robust. This improves error handling and user experience. Here's how you can enhance it:

```python
def get_user_age():
    while True:
        try:
            age = int(input("Enter your age: "))
            if age >= 0:
                return age
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
```"""
        },
        {
            "name": "AI response without clear code block",
            "original_comment": "Function lacks documentation",
            "ai_response": """Your function works well! Adding documentation would enhance readability and help other developers understand your code better. Documentation improves maintainability and follows Python conventions. You could add a docstring explaining what the function does, its parameters, and return value."""
        },
        {
            "name": "Minimal AI response",
            "original_comment": "No error handling",
            "ai_response": """Add try-catch blocks for better error handling. This improves robustness."""
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"{'='*80}")
        print(f"TEST {i}: {test_case['name']}")
        print(f"{'='*80}")
        
        print("Input:")
        print(f"Original Comment: {test_case['original_comment']}")
        print(f"AI Response: {test_case['ai_response']}")
        print("\n" + "-"*60)
        
        markdown_section = create_markdown_section(
            test_case['original_comment'], 
            test_case['ai_response']
        )
        
        print("Generated Markdown Section:")
        print(markdown_section)
        print("-"*60 + "\n")
    
    print("All test cases completed!")


def demo_full_workflow():
    """
    Demonstrate a complete workflow from comment to markdown.
    """
    print("="*80)
    print("DEMO: Complete Workflow")
    print("="*80)
    
    # Sample data
    original_comment = "This function doesn't handle edge cases"
    
    # Simulated AI response (this would come from calling the AI)
    ai_response = """I appreciate the solid foundation of your function! Here's an opportunity to enhance its robustness by handling edge cases.

Adding edge case handling improves reliability because it prevents unexpected crashes and provides better user experience when dealing with unusual inputs.

Here's an improved version:

```python
def process_data(data):
    # Handle edge cases
    if not data:
        return []
    
    if not isinstance(data, list):
        raise TypeError("Input must be a list")
    
    result = []
    for item in data:
        if isinstance(item, (int, float)) and item > 0:
            result.append(item * 2)
    
    return result
```

This enhancement makes your code much more robust and professional!"""
    
    print(f"Original Comment: {original_comment}")
    print(f"\nAI Response:\n{ai_response}")
    print("\n" + "="*60)
    
    markdown = create_markdown_section(original_comment, ai_response)
    
    print("Generated Markdown:")
    print(markdown)
    
    # Also save to file for demonstration
    with open("sample_markdown_output.md", "w") as f:
        f.write("# Code Review Feedback\n\n")
        f.write(markdown)
    
    print("✓ Markdown also saved to 'sample_markdown_output.md'")


if __name__ == "__main__":
    test_create_markdown_section()
    demo_full_workflow()
