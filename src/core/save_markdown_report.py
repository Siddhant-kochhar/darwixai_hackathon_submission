import os
from pathlib import Path
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


def save_markdown_report(report, filename):
    """
    Saves a Markdown report to a specified file.
    
    Args:
        report (str): The Markdown content to save
        filename (str): The path/filename where the report should be saved
    
    Returns:
        bool: True if successful, False otherwise
    
    Raises:
        ValueError: If report is None or empty, or filename is invalid
        OSError: If there are file system related errors
    """
    # Input validation
    if not report or not isinstance(report, str):
        raise ValueError("Report must be a non-empty string")
    
    if not filename or not isinstance(filename, str):
        raise ValueError("Filename must be a non-empty string")
    
    try:
        # Convert to Path object for better path handling
        file_path = Path(filename)
        
        # Create parent directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the markdown content to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Markdown report successfully saved to: {file_path.absolute()}")
        return True
        
    except PermissionError as e:
        print(f"Permission denied: Unable to write to {filename}")
        print(f"Error details: {e}")
        return False
        
    except FileNotFoundError as e:
        print(f"Invalid file path: {filename}")
        print(f"Error details: {e}")
        return False
        
    except OSError as e:
        print(f"File system error occurred while saving to {filename}")
        print(f"Error details: {e}")
        return False
        
    except Exception as e:
        print(f"Unexpected error occurred while saving markdown report")
        print(f"Error details: {e}")
        return False


import google.generativeai as genai
from .empathetic_code_reviewer import read_input_json, generate_ai_prompt, create_markdown_section


def save_markdown_report(report, filename):
    """
    Saves a Markdown report to a specified file.
    
    Args:
        report (str): The Markdown content to save
        filename (str): The path/filename where the report should be saved
    
    Returns:
        bool: True if successful, False otherwise
    
    Raises:
        ValueError: If report is None or empty, or filename is invalid
        OSError: If there are file system related errors
    """
    # Input validation
    if not report or not isinstance(report, str):
        raise ValueError("Report must be a non-empty string")
    
    if not filename or not isinstance(filename, str):
        raise ValueError("Filename must be a non-empty string")
    
    try:
        # Convert to Path object for better path handling
        file_path = Path(filename)
        
        # Create parent directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the markdown content to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Markdown report successfully saved to: {file_path.absolute()}")
        return True
        
    except PermissionError as e:
        print(f"Permission denied: Unable to write to {filename}")
        print(f"Error details: {e}")
        return False
        
    except FileNotFoundError as e:
        print(f"Invalid file path: {filename}")
        print(f"Error details: {e}")
        return False
        
    except OSError as e:
        print(f"File system error occurred while saving to {filename}")
        print(f"Error details: {e}")
        return False
        
    except Exception as e:
        print(f"Unexpected error occurred while saving markdown report")
        print(f"Error details: {e}")
        return False


def generate_full_report(review_data):
    """
    Generate a complete Markdown report from review data.
    
    Args:
        review_data (dict): Dictionary containing 'code_snippet' and 'review_comments'
    
    Returns:
        str: Complete Markdown report with all sections
    
    Raises:
        ValueError: If review_data is invalid
        Exception: If AI API calls fail
    """
    # Validate input
    if not isinstance(review_data, dict):
        raise ValueError("review_data must be a dictionary")
    
    if 'code_snippet' not in review_data or 'review_comments' not in review_data:
        raise ValueError("review_data must contain 'code_snippet' and 'review_comments' keys")
    
    code_snippet = review_data['code_snippet']
    review_comments = review_data['review_comments']
    
    if not isinstance(code_snippet, str) or not isinstance(review_comments, list):
        raise ValueError("Invalid data types in review_data")
    
    # Initialize Gemini AI with optimized settings
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Warning: GEMINI_API_KEY not set. Using simulated responses for demonstration.")
        use_ai = False
    else:
        try:
            genai.configure(api_key=api_key)
            # Configure model with faster settings
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 800,  # Reduced for faster generation
                "response_mime_type": "text/plain",
            }
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                generation_config=generation_config
            )
            use_ai = True
            print("✅ Successfully connected to Gemini AI with optimized settings")
        except Exception as e:
            print(f"Warning: Could not initialize Gemini AI: {e}")
            print("Using simulated responses for demonstration.")
            use_ai = False
    
    # Start building the report according to hackathon specifications
    report = "# 🤖 Empathetic Code Review Report\n\n"
    report += f"**Generated on:** {os.popen('date').read().strip()}\n"
    report += f"**Tagline:** *Transforming Critical Feedback into Constructive Growth*\n\n"
    
    # Add code section
    report += "## 📝 Code Under Review\n\n"
    report += "```python\n"
    report += code_snippet.strip() + "\n"
    report += "```\n\n"
    
    # Add summary
    report += "## 📊 Summary\n\n"
    report += f"This report analyzes **{len(review_comments)} review comment(s)** and transforms them into empathetic, "
    report += "constructive guidance. Each comment has been reframed to focus on learning opportunities while "
    report += "maintaining technical accuracy and providing clear explanations of the underlying principles.\n\n"
    
    # Add detailed analysis section
    report += "## 🎯 Detailed Analysis\n\n"
    
    # Process comments concurrently for faster generation
    def process_single_comment(comment_data):
        i, comment = comment_data
        print(f"Processing comment {i}/{len(review_comments)}: {comment}")
        
        # Generate AI prompt with hackathon specifications
        prompt = generate_enhanced_ai_prompt(code_snippet, comment)
        
        # Get AI response (real or simulated)
        if use_ai:
            try:
                start_time = time.time()
                response = model.generate_content(prompt)
                ai_response = response.text
                duration = time.time() - start_time
                print(f"✅ Received AI response for comment {i} ({duration:.1f}s)")
            except Exception as e:
                print(f"Error getting AI response for comment {i}: {e}")
                ai_response = create_enhanced_fallback_response(comment, code_snippet)
        else:
            # Enhanced simulated response that follows hackathon format
            ai_response = create_enhanced_simulated_response(comment, code_snippet)
        
        # Create markdown section with proper formatting
        markdown_section = create_enhanced_markdown_section(comment, ai_response)
        return i, markdown_section
    
    # Process comments in parallel for faster execution
    if use_ai and len(review_comments) > 1:
        print(f"🚀 Processing {len(review_comments)} comments concurrently...")
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=min(3, len(review_comments))) as executor:
            # Submit all tasks
            comment_data = [(i, comment) for i, comment in enumerate(review_comments, 1)]
            future_to_comment = {executor.submit(process_single_comment, data): data for data in comment_data}
            
            # Collect results in order
            results = {}
            for future in as_completed(future_to_comment):
                try:
                    i, markdown_section = future.result(timeout=30)  # 30 second timeout per comment
                    results[i] = markdown_section
                except Exception as e:
                    comment_data = future_to_comment[future]
                    i, comment = comment_data
                    print(f"Error processing comment {i}: {e}")
                    # Fallback response
                    results[i] = create_enhanced_markdown_section(comment, create_enhanced_fallback_response(comment, code_snippet))
            
            # Add results in order
            for i in range(1, len(review_comments) + 1):
                report += results.get(i, "")
        
        total_time = time.time() - start_time
        print(f"⚡ Completed all comments in {total_time:.1f}s (avg: {total_time/len(review_comments):.1f}s per comment)")
    else:
        # Sequential processing for single comment or fallback
        for i, comment in enumerate(review_comments, 1):
            markdown_section = process_single_comment((i, comment))[1]
            report += markdown_section
    
    # Add holistic summary as per hackathon requirements
    report += "\n## 🎉 Holistic Summary\n\n"
    report += "**Excellent work on your code!** The suggestions above represent opportunities to elevate your already solid foundation. "
    report += "Each recommendation focuses on fundamental software development principles like performance optimization, code readability, "
    report += "and maintainability. Remember, even experienced developers constantly refine their code - it's a sign of growth, not weakness. "
    report += "These improvements will make your code more professional, efficient, and easier for your future self and teammates to understand. "
    report += "Keep up the fantastic work and continue embracing the learning journey! 🚀\n\n"
    
    # Add footer
    report += "---\n"
    report += "*Report generated by Empathetic Code Reviewer | Transforming Critical Feedback into Constructive Growth*\n"
    
    return report


def generate_enhanced_ai_prompt(code_snippet: str, comment: str) -> str:
    """
    Generate an optimized AI prompt for faster processing.
    """
    prompt = f"""Transform this code review comment into empathetic feedback:

**Code:**
```python
{code_snippet.strip()}
```

**Critical comment:** {comment.strip()}

**Transform into:**
- Positive Rephrasing: [Encouraging version]
- The 'Why': [Explain the principle briefly]
- Suggested Improvement: [Show code example]

Keep response concise but helpful. Use encouraging tone. Include practical code fix."""

    return prompt


def create_enhanced_simulated_response(comment: str, code_snippet: str) -> str:
    """
    Create a high-quality simulated response that follows hackathon requirements.
    """
    # Enhanced responses based on common code review patterns
    if "inefficient" in comment.lower() or "performance" in comment.lower():
        return """Positive Rephrasing: Great start on the logic here! For better performance, especially with larger datasets, we can make this more efficient by optimizing our approach.

The 'Why': When working with collections, the way we iterate and filter can significantly impact performance. List comprehensions and built-in functions are often more efficient because they're optimized at the C level in Python, making them faster than manual loops for most operations.

Suggested Improvement:
```python
def get_active_users(users):
    return [user for user in users if user.is_active and user.profile_complete]
```
This approach combines filtering and collection in a single, readable operation that's typically faster and more Pythonic."""

    elif "variable" in comment.lower() and ("name" in comment.lower() or "bad" in comment.lower()):
        return """Positive Rephrasing: Nice work on the functionality! Let's enhance readability by using more descriptive variable names - this is one of those small changes that makes a huge difference for code maintenance.

The 'Why': Clear variable names are crucial for code maintainability. When we return to code months later, or when teammates review it, descriptive names immediately communicate intent. This reduces cognitive load and prevents bugs caused by misunderstanding variable purposes.

Suggested Improvement:
```python
def process_data(data):
    result = []
    for user_item in data:  # or 'user', 'item', 'record' - whatever fits the context
        result.append(user_item * 2)
    return result
```
Even better, consider what the variable represents: if it's user data, call it 'user'; if it's a number, call it 'value' or 'number'."""

    elif "docstring" in comment.lower() or "documentation" in comment.lower():
        return """Positive Rephrasing: Excellent implementation! Adding documentation will make this professional-grade code that any developer (including your future self) will appreciate.

The 'Why': Documentation serves as a contract for your function, explaining what it does, what it expects, and what it returns. This is essential for team collaboration, code maintenance, and following Python conventions (PEP 257). Good docs prevent bugs and save hours of code-reading time.

Suggested Improvement:
```python
def calculate_area(radius):
    '''
    Calculate the area of a circle given its radius.
    
    Args:
        radius (float): The radius of the circle
        
    Returns:
        float: The area of the circle
    '''
    return 3.14 * radius * radius
```
This follows Python documentation standards and makes your code self-explanatory."""

    elif "boolean" in comment.lower() and "true" in comment.lower():
        return """Positive Rephrasing: Great logic structure! We can make this even cleaner by leveraging Python's natural boolean evaluation - it's a neat language feature that makes code more readable.

The 'Why': In Python, comparing boolean values to True/False is redundant because the values are already boolean. Removing '== True' makes code more concise and follows Python's principle of readability. It also prevents potential issues if the value isn't exactly True but is truthy.

Suggested Improvement:
```python
if user.is_active and user.profile_complete:
    # This is cleaner and more Pythonic
```
Python's boolean evaluation is designed to handle these cases elegantly, making your code both shorter and more idiomatic."""

    else:
        # Generic enhanced response
        return f"""Positive Rephrasing: Solid work on this implementation! Here's an opportunity to enhance your code by addressing: {comment.lower()}.

The 'Why': This suggestion improves code quality by focusing on fundamental software principles like maintainability, readability, and following established best practices. These improvements make code more professional and easier to work with in team environments.

Suggested Improvement:
```python
# Enhanced version addressing: {comment}
# Implementation would depend on the specific improvement needed
def improved_function():
    # Your enhanced code here
    pass
```
This type of refinement is what separates good code from great code - attention to these details shows professional development practices."""


def create_enhanced_markdown_section(original_comment: str, ai_response: str) -> str:
    """
    Create a properly formatted markdown section following hackathon specifications.
    """
    # Parse AI response to extract components
    lines = ai_response.strip().split('\n')
    positive_rephrasing = ""
    why_explanation = ""
    suggested_improvement = ""
    
    current_section = None
    code_block = []
    in_code_block = False
    
    for line in lines:
        line = line.strip()
        
        if line.startswith("Positive Rephrasing:"):
            current_section = "positive"
            positive_rephrasing = line.replace("Positive Rephrasing:", "").strip()
        elif line.startswith("The 'Why':"):
            current_section = "why"
            why_explanation = line.replace("The 'Why':", "").strip()
        elif line.startswith("Suggested Improvement:"):
            current_section = "improvement"
            suggested_improvement = line.replace("Suggested Improvement:", "").strip()
        elif line.startswith("```"):
            if in_code_block:
                in_code_block = False
                if code_block:
                    suggested_improvement += "\n```python\n" + "\n".join(code_block) + "\n```"
                    code_block = []
            else:
                in_code_block = True
        elif in_code_block:
            code_block.append(line)
        elif line and current_section:
            if current_section == "positive" and not positive_rephrasing:
                positive_rephrasing = line
            elif current_section == "positive":
                positive_rephrasing += " " + line
            elif current_section == "why" and not why_explanation:
                why_explanation = line
            elif current_section == "why":
                why_explanation += " " + line
            elif current_section == "improvement" and not suggested_improvement:
                suggested_improvement = line
            elif current_section == "improvement" and not line.startswith("```"):
                suggested_improvement += " " + line
    
    # Fallback parsing if structured parsing fails
    if not positive_rephrasing:
        sentences = ai_response.split('.')
        positive_rephrasing = sentences[0] + "." if sentences else "Great observation! Here's an opportunity to enhance your code."
    
    if not why_explanation:
        why_explanation = "This improvement enhances code quality by following software development best practices and principles."
    
    if not suggested_improvement:
        suggested_improvement = "```python\n# Enhanced code example would be provided here\n```"
    
    # Create the formatted markdown section
    markdown_section = f"""---
### 💡 Analysis of Comment: "{original_comment}"

* **🎯 Positive Rephrasing:** {positive_rephrasing}

* **🧠 The 'Why':** {why_explanation}

* **⚡ Suggested Improvement:**
{suggested_improvement}

"""
    
    return markdown_section


def create_enhanced_fallback_response(comment: str, code_snippet: str) -> str:
    """
    Create a high-quality fallback response when AI is not available.
    This provides specific responses based on comment patterns.
    """
    comment_lower = comment.lower()
    
    # Efficiency/Performance related comments
    if any(word in comment_lower for word in ['inefficient', 'performance', 'slow', 'loop', 'optimize']):
        if 'get_active_users' in code_snippet:
            return """Positive Rephrasing: Great start on the logic here! For better performance, especially with large user lists, we can make this more efficient by combining the filtering operations.

The 'Why': When working with collections, manual loops can become slow as datasets grow. List comprehensions are optimized at the C level in Python, making them faster and more readable. They also reduce the cognitive load by expressing the intent more clearly - "get all users where conditions are met" rather than "loop through users, check conditions, append to results."

Suggested Improvement:
```python
def get_active_users(users):
    return [user for user in users if user.is_active and user.profile_complete]
```
This approach is not only faster but also more Pythonic and easier to read. The intent is immediately clear, and it eliminates the need for temporary variables."""
        else:
            return """Positive Rephrasing: Excellent logic foundation! Let's optimize this for better performance, especially when dealing with larger datasets.

The 'Why': Performance optimization is crucial for scalable applications. Efficient algorithms and data structures can make the difference between an application that handles 100 records vs 100,000 records smoothly.

Suggested Improvement:
```python
# Consider using list comprehensions, built-in functions, or more efficient algorithms
# Specific optimization would depend on the particular inefficiency identified
```
Performance improvements often involve choosing the right data structures and algorithms for the task."""

    # Variable naming issues
    elif any(word in comment_lower for word in ['variable', 'name', 'naming', "'u'"]):
        return """Positive Rephrasing: Nice work on the functionality! Let's enhance readability with more descriptive variable names - this small change makes a huge difference for code maintenance.

The 'Why': Clear variable names are one of the most important aspects of clean code. When you or a teammate returns to this code months later, descriptive names immediately communicate intent and reduce the time needed to understand the logic. Good naming prevents bugs and makes code self-documenting.

Suggested Improvement:
```python
def get_active_users(users):
    results = []
    for user in users:  # Much clearer than 'u'
        if user.is_active and user.profile_complete:
            results.append(user)
    return results
```
Using 'user' instead of 'u' immediately tells us what we're working with. This follows the principle that code is read far more often than it's written."""

    # Boolean comparison issues
    elif any(word in comment_lower for word in ['boolean', 'true', 'false', 'redundant', '== true']):
        return """Positive Rephrasing: Great logic structure! We can make this even cleaner by leveraging Python's natural boolean evaluation - it's one of those elegant language features that makes code more readable.

The 'Why': In Python, boolean values are already True or False, so comparing them to True/False is redundant. This follows Python's principle of readability and can prevent subtle bugs if the value is truthy but not exactly True. It also makes the code more concise and idiomatic.

Suggested Improvement:
```python
def get_active_users(users):
    results = []
    for user in users:
        if user.is_active and user.profile_complete:  # Clean and Pythonic
            results.append(user)
    return results
```
Python's boolean evaluation naturally handles this, making the code cleaner and following the Zen of Python: "Simple is better than complex."""

    # Documentation/docstring issues
    elif any(word in comment_lower for word in ['docstring', 'documentation', 'comment', 'document']):
        return """Positive Rephrasing: Excellent implementation! Adding documentation will transform this into professional-grade code that any developer (including your future self) will appreciate.

The 'Why': Documentation serves as a contract for your function, clearly stating what it does, what it expects, and what it returns. This is essential for team collaboration, code maintenance, and follows Python conventions (PEP 257). Good documentation prevents bugs and saves hours of code-reading time.

Suggested Improvement:
```python
def get_active_users(users):
    '''
    Filter users to return only those who are active and have complete profiles.
    
    Args:
        users (list): List of user objects to filter
        
    Returns:
        list: Filtered list containing only active users with complete profiles
    '''
    return [user for user in users if user.is_active and user.profile_complete]
```
This follows Python documentation standards and makes your code self-explanatory and professional."""

    # Generic fallback
    else:
        return f"""Positive Rephrasing: Thank you for this valuable feedback! Here's an opportunity to enhance the code quality and follow best practices.

The 'Why': This suggestion focuses on improving code maintainability, readability, and following established software development principles. These improvements make code more professional and easier to work with in team environments.

Suggested Improvement:
```python
# Enhanced implementation addressing: {comment}
# Specific improvements would be tailored to the exact feedback provided
```
Continuous code improvement is a hallmark of professional development and shows attention to software craftsmanship."""


def create_fallback_response(comment: str, code_snippet: str) -> str:
    """
    Create a fallback response when AI is not available.
    """
    return create_enhanced_fallback_response(comment, code_snippet)


def main():
    """
    Main function that orchestrates the complete workflow:
    1. Reads input JSON using read_input_json()
    2. Calls generate_full_report() to produce the Markdown report
    3. Saves the report using save_markdown_report()
    4. Prints a success message with the filename of the generated report
    """
    try:
        # Step 1: Read input JSON
        input_filename = "sample_review.json"
        print(f"Step 1: Reading input from '{input_filename}'...")
        
        if not os.path.exists(input_filename):
            print(f"Warning: {input_filename} not found. Creating sample data...")
            # Create sample data for demonstration
            sample_data = {
                "code_snippet": """def calculate_area(radius):
    return 3.14 * radius * radius

def get_user_input():
    radius = input("Enter radius: ")
    return radius""",
                "review_comments": [
                    "Consider using math.pi instead of hardcoded 3.14",
                    "The function get_user_input should validate input and convert to float",
                    "Add docstrings to explain what each function does",
                    "Consider error handling for invalid inputs"
                ]
            }
            
            import json
            with open(input_filename, 'w') as f:
                json.dump(sample_data, f, indent=2)
            print(f"Created sample data in '{input_filename}'")
        
        review_data = read_input_json(input_filename)
        print(f"✓ Successfully loaded review data with {len(review_data['review_comments'])} comments")
        
        # Step 2: Generate the full report
        print("\nStep 2: Generating full Markdown report...")
        markdown_report = generate_full_report(review_data)
        print("✓ Successfully generated complete Markdown report")
        
        # Step 3: Save the report
        output_filename = "empathetic_code_review_report.md"
        print(f"\nStep 3: Saving report to '{output_filename}'...")
        
        success = save_markdown_report(markdown_report, output_filename)
        
        if success:
            # Step 4: Print success message
            print(f"\n🎉 SUCCESS! Code review report has been generated and saved.")
            print(f"📄 Report filename: {output_filename}")
            print(f"📊 Report contains {len(review_data['review_comments'])} detailed analyses")
            print(f"📍 Full path: {os.path.abspath(output_filename)}")
            
            # Show a preview of the report
            print(f"\n📋 Report Preview (first 300 characters):")
            print("-" * 50)
            print(markdown_report[:300] + "..." if len(markdown_report) > 300 else markdown_report)
            print("-" * 50)
            
        else:
            print("❌ Failed to save the report. Check the error messages above.")
            
    except Exception as e:
        print(f"❌ Error in main workflow: {e}")
        print("Please check your input file and try again.")


# Example usage and testing
if __name__ == "__main__":
    main()