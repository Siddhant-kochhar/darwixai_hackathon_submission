#!/usr/bin/env python3
"""
Test script for the generate_ai_prompt function
"""

from empathetic_code_reviewer import generate_ai_prompt


def test_generate_ai_prompt():
    """
    Test the generate_ai_prompt function with various code snippets and comments.
    """
    print("Testing generate_ai_prompt function...\n")
    
    # Test cases with different types of code issues
    test_cases = [
        {
            "name": "Hardcoded values",
            "code": """def calculate_area(radius):
    return 3.14 * radius * radius""",
            "comment": "Don't use hardcoded 3.14, use math.pi instead"
        },
        {
            "name": "Input validation",
            "code": """def get_user_age():
    age = input("Enter your age: ")
    return age""",
            "comment": "This function doesn't validate input or convert to int"
        },
        {
            "name": "Exception handling",
            "code": """def divide_numbers(a, b):
    return a / b""",
            "comment": "No error handling for division by zero"
        },
        {
            "name": "Code documentation",
            "code": """def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result""",
            "comment": "Missing docstring and unclear variable names"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"{'='*60}")
        print(f"TEST {i}: {test_case['name']}")
        print(f"{'='*60}")
        
        prompt = generate_ai_prompt(test_case['code'], test_case['comment'])
        
        print("Generated AI Prompt:")
        print("-" * 40)
        print(prompt)
        print("\n")
    
    print("All test cases completed!")
    print("\nThe generated prompts are ready to send to Google Gemini or other LLMs.")


def demo_single_prompt():
    """
    Demonstrate a single prompt generation for clarity.
    """
    print("\n" + "="*80)
    print("DEMO: Single Prompt Generation")
    print("="*80)
    
    code = """def login_user(username, password):
    if username == "admin" and password == "password123":
        return True
    return False"""
    
    comment = "Hardcoded credentials are a security risk"
    
    prompt = generate_ai_prompt(code, comment)
    
    print("Input Code:")
    print(code)
    print("\nInput Comment:")
    print(comment)
    print("\nGenerated Prompt:")
    print("-" * 50)
    print(prompt)
    print("-" * 50)


if __name__ == "__main__":
    test_generate_ai_prompt()
    demo_single_prompt()
