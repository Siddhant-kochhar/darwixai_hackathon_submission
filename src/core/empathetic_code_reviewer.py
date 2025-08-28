#!/usr/bin/env python3
"""
Empathetic Code Reviewer

A Python script that reads code snippets and review comments, then uses an AI model
to generate empathetic feedback for code reviews.
"""

import json
import os
from typing import Dict, List, Any, Optional
import google.generativeai as genai
from pathlib import Path


def read_input_json(file_path: str) -> Dict[str, Any]:
    """
    Read and parse a JSON file containing code review data.
    
    Args:
        file_path: Path to the JSON file to read.
        
    Returns:
        Dictionary with keys 'code_snippet' and 'review_comments'.
        
    Raises:
        FileNotFoundError: If the file doesn't exist.
        json.JSONDecodeError: If the file contains invalid JSON.
        KeyError: If required keys 'code_snippet' or 'review_comments' are missing.
        ValueError: If the data structure is invalid.
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read and parse JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Validate that data is a dictionary
        if not isinstance(data, dict):
            raise ValueError("JSON file must contain a dictionary object")
        
        # Check for required keys
        if 'code_snippet' not in data:
            raise KeyError("Missing required key 'code_snippet' in JSON data")
        
        if 'review_comments' not in data:
            raise KeyError("Missing required key 'review_comments' in JSON data")
        
        # Validate data types
        if not isinstance(data['code_snippet'], str):
            raise ValueError("'code_snippet' must be a string")
        
        if not isinstance(data['review_comments'], list):
            raise ValueError("'review_comments' must be a list")
        
        # Validate that review_comments contains strings
        for i, comment in enumerate(data['review_comments']):
            if not isinstance(comment, str):
                raise ValueError(f"review_comments[{i}] must be a string, got {type(comment).__name__}")
        
        return {
            'code_snippet': data['code_snippet'],
            'review_comments': data['review_comments']
        }
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{file_path}': {e}")
        raise
    except (KeyError, ValueError) as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error reading file '{file_path}': {e}")
        raise


def generate_ai_prompt(code_snippet: str, comment: str) -> str:
    """
    Generate an AI prompt for empathetic code review based on a single code snippet and comment.
    Follows hackathon specifications for transforming critical feedback into constructive growth.
    
    Args:
        code_snippet: The code to be reviewed.
        comment: A single review comment or suggestion.
        
    Returns:
        A formatted string prompt ready to send to an LLM like Google Gemini.
        
    The prompt instructs the AI to:
    1. Rephrase the comment positively and encouragingly
    2. Explain why the suggestion matters (performance, readability, Python conventions)
    3. Provide a concrete improved code example with explanation
    """
    prompt = f"""You are an empathetic senior developer and mentor participating in "The Empathetic Code Reviewer" mission. Your goal is to transform critical feedback into constructive growth opportunities.

**Mission:** Transform critical code review feedback into empathetic, educational guidance that helps developers learn while building their confidence.

**Code being reviewed:**
```python
{code_snippet.strip()}
```

**Original critical comment:** "{comment.strip()}"

**Your task:** Rewrite this feedback following these requirements:

1. **Positive Rephrasing**: Transform the criticism into encouraging, supportive feedback that acknowledges effort while suggesting improvement
2. **The 'Why'**: Explain the underlying software principle (performance, readability, maintainability, Python conventions, security, etc.)
3. **Suggested Improvement**: Provide a concrete code example that demonstrates the recommended fix with a brief explanation

**Guidelines:**
- Start with positive acknowledgment ("Great start!", "Nice logic!", "Good thinking here!")
- Use encouraging language that builds confidence
- Be specific about WHY the change matters
- Include practical code examples
- Focus on learning and growth
- Maintain a mentoring, supportive tone
- Consider the developer's skill level and provide appropriate explanations

**Example response format:**
"[Positive acknowledgment and encouraging reframe of the feedback]

[Clear explanation of the software principle and why it matters - be specific about benefits like performance, maintainability, readability, security, etc.]

Here's how you can enhance this:

```python
[Concrete improved code example]
```

[Brief explanation of what makes this better and any additional tips]"

Please generate your empathetic, educational response that transforms the critical feedback into constructive guidance:"""

    return prompt


def create_markdown_section(original_comment: str, ai_response: str) -> str:
    """
    Create a Markdown-formatted section from an original comment and AI response.
    
    Args:
        original_comment: The original review comment.
        ai_response: The AI's empathetic response containing rephrasing, explanation, and code.
        
    Returns:
        A Markdown-formatted string with structured sections.
        
    The function attempts to parse the AI response and extract:
    - Positive rephrasing of the comment
    - Educational explanation of why the suggestion matters
    - Improved code example
    """
    # Clean up the inputs
    original_comment = original_comment.strip()
    ai_response = ai_response.strip()
    
    # Initialize extracted sections
    positive_rephrasing = ""
    why_explanation = ""
    improved_code = ""
    
    # Try to extract sections from AI response
    # This is a simple parsing approach - could be enhanced based on AI response patterns
    lines = ai_response.split('\n')
    
    # Look for common patterns in AI responses
    current_section = None
    code_block_started = False
    code_lines = []
    
    for line in lines:
        line_lower = line.lower().strip()
        
        # Detect positive rephrasing section
        if any(keyword in line_lower for keyword in ['opportunity', 'enhance', 'improve', 'better way', 'consider', 'suggestion']):
            if not positive_rephrasing and len(line.strip()) > 20:  # Avoid short lines
                positive_rephrasing = line.strip()
        
        # Detect explanation section
        elif any(keyword in line_lower for keyword in ['because', 'this helps', 'this improves', 'performance', 'readability', 'maintainability', 'convention']):
            if not why_explanation and len(line.strip()) > 20:
                why_explanation = line.strip()
        
        # Detect code blocks
        elif '```python' in line_lower:
            code_block_started = True
            continue
        elif '```' in line and code_block_started:
            code_block_started = False
            if code_lines:
                improved_code = '\n'.join(code_lines)
            continue
        elif code_block_started:
            code_lines.append(line)
    
    # Fallback: if we couldn't extract specific sections, use the full response intelligently
    if not positive_rephrasing:
        # Take the first substantial sentence as positive rephrasing
        sentences = [s.strip() for s in ai_response.split('.') if len(s.strip()) > 20]
        if sentences:
            positive_rephrasing = sentences[0] + '.'
        else:
            positive_rephrasing = "Here's an opportunity to enhance your code"
    
    if not why_explanation:
        # Look for explanatory content
        sentences = [s.strip() for s in ai_response.split('.') if any(word in s.lower() for word in ['performance', 'readability', 'maintainability', 'best practice', 'convention'])]
        if sentences:
            why_explanation = sentences[0] + '.'
        else:
            why_explanation = "This improvement enhances code quality and follows Python best practices"
    
    if not improved_code:
        # If no code block found, indicate that code example should be provided
        improved_code = "# Improved code example would be provided by the AI response"
    
    # Create the Markdown section
    markdown_section = f"""---
### Analysis of Comment: "{original_comment}"

* **Positive Rephrasing:** {positive_rephrasing}

* **The 'Why':** {why_explanation}

* **Suggested Improvement:**
```python
{improved_code}
```

"""
    
    return markdown_section


class EmpathethicCodeReviewer:
    """
    A class to handle empathetic code review generation using AI models.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the code reviewer with Gemini API.
        
        Args:
            api_key: Gemini API key. If None, will try to get from environment variable.
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key not provided. Set GEMINI_API_KEY environment variable or pass api_key parameter.")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def load_review_data(self, file_path: str) -> Dict[str, Any]:
        """
        Load code review data from a JSON file.
        
        Args:
            file_path: Path to the JSON file containing review data.
            
        Returns:
            Dictionary containing code_snippet and review_comments.
            
        Raises:
            FileNotFoundError: If the file doesn't exist.
            json.JSONDecodeError: If the file contains invalid JSON.
            KeyError: If required keys are missing from the JSON.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Validate required fields
            if 'code_snippet' not in data:
                raise KeyError("Missing 'code_snippet' field in JSON data")
            if 'review_comments' not in data:
                raise KeyError("Missing 'review_comments' field in JSON data")
            
            return data
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Review data file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in file {file_path}: {e}")
    
    def create_review_data(self, code_snippet: str, review_comments: List[str]) -> Dict[str, Any]:
        """
        Create review data dictionary from code snippet and comments.
        
        Args:
            code_snippet: The code to be reviewed.
            review_comments: List of review comments.
            
        Returns:
            Dictionary containing the review data.
        """
        return {
            "code_snippet": code_snippet,
            "review_comments": review_comments
        }
    
    def generate_empathetic_feedback(self, review_data: Dict[str, Any]) -> str:
        """
        Generate empathetic feedback for code review using AI.
        
        Args:
            review_data: Dictionary containing code_snippet and review_comments.
            
        Returns:
            Empathetic feedback as a string.
        """
        code_snippet = review_data.get('code_snippet', '')
        review_comments = review_data.get('review_comments', [])
        
        # Create empathetic prompt
        prompt = self._create_empathetic_prompt(code_snippet, review_comments)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating feedback: {str(e)}"
    
    def _create_empathetic_prompt(self, code_snippet: str, review_comments: List[str]) -> str:
        """
        Create an empathetic prompt for the AI model.
        
        Args:
            code_snippet: The code being reviewed.
            review_comments: List of review comments.
            
        Returns:
            Formatted prompt string.
        """
        comments_text = "\n".join([f"- {comment}" for comment in review_comments])
        
        prompt = f"""
As an empathetic and constructive code reviewer, please provide feedback that is:
- Encouraging and supportive
- Focused on learning and improvement
- Respectful of the developer's effort
- Specific and actionable
- Balanced with positive observations

Code to review:
```
{code_snippet}
```

Current review comments:
{comments_text}

Please provide empathetic feedback that addresses these comments while maintaining a positive and constructive tone. Focus on:
1. Acknowledging the effort and good aspects of the code
2. Explaining the 'why' behind suggestions
3. Offering specific, actionable improvements
4. Encouraging continued learning and growth
5. Being respectful and kind in delivery

Generate your empathetic review response:
"""
        return prompt
    
    def save_feedback(self, feedback: str, output_path: str) -> None:
        """
        Save the generated feedback to a file.
        
        Args:
            feedback: The feedback text to save.
            output_path: Path where to save the feedback.
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(feedback)
            print(f"Feedback saved to: {output_path}")
        except Exception as e:
            print(f"Error saving feedback: {str(e)}")


def main():
    """
    Main function to demonstrate the empathetic code reviewer.
    """
    try:
        # Initialize the reviewer
        reviewer = EmpathethicCodeReviewer()
        
        # Example: Load review data from JSON file using the new read_input_json function
        json_file_path = "sample_review.json"
        
        if os.path.exists(json_file_path):
            print(f"Loading review data from {json_file_path}...")
            # Use the new read_input_json function
            review_data = read_input_json(json_file_path)
            print("✓ Successfully loaded review data using read_input_json function")
        else:
            # Create sample data programmatically
            print("Creating sample review data...")
            sample_code = '''
def calculate_area(radius):
    return 3.14 * radius * radius

def get_user_input():
    radius = input("Enter radius: ")
    return radius
'''
            sample_comments = [
                "Consider using math.pi instead of hardcoded 3.14",
                "The function get_user_input should validate input and convert to float",
                "Add docstrings to explain what each function does",
                "Consider error handling for invalid inputs"
            ]
            
            review_data = reviewer.create_review_data(sample_code, sample_comments)
            
            # Save sample data for future use
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(review_data, f, indent=2)
            print(f"Sample review data created and saved to {json_file_path}")
            
            # Demonstrate reading the file we just created
            print(f"Now testing read_input_json function with {json_file_path}...")
            test_data = read_input_json(json_file_path)
            print("✓ Successfully tested read_input_json function")
        
        # Demonstrate generate_ai_prompt function
        print("\n" + "="*60)
        print("DEMONSTRATING generate_ai_prompt FUNCTION")
        print("="*60)
        
        # Test with the first comment from the review data
        if review_data['review_comments']:
            first_comment = review_data['review_comments'][0]
            prompt = generate_ai_prompt(review_data['code_snippet'], first_comment)
            
            print(f"Single comment: {first_comment}")
            print("\nGenerated AI prompt:")
            print("-" * 40)
            print(prompt[:200] + "..." if len(prompt) > 200 else prompt)
            print("-" * 40)
            print("✓ Successfully generated AI prompt for individual comment")
        
        # Generate empathetic feedback using the class method
        print("\nGenerating empathetic feedback using class method...")
        feedback = reviewer.generate_empathetic_feedback(review_data)
        
        # Display the feedback
        print("\n" + "="*60)
        print("EMPATHETIC CODE REVIEW FEEDBACK")
        print("="*60)
        print(feedback)
        print("="*60)
        
        # Save feedback to file
        output_file = "empathetic_feedback.txt"
        reviewer.save_feedback(feedback, output_file)
        
    except Exception as e:
        print(f"Error in main execution: {str(e)}")
        print("Make sure to set your GEMINI_API_KEY environment variable.")


if __name__ == "__main__":
    main()
