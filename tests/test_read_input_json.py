#!/usr/bin/env python3
"""
Test script for the read_input_json function
"""

from empathetic_code_reviewer import read_input_json
import json
import os


def test_read_input_json():
    """
    Test the read_input_json function with various scenarios.
    """
    print("Testing read_input_json function...\n")
    
    # Test 1: Valid JSON file
    print("Test 1: Reading valid JSON file")
    try:
        result = read_input_json("sample_review.json")
        print(f"✓ Success! Loaded data with {len(result['review_comments'])} comments")
        print(f"  Code snippet preview: {result['code_snippet'][:50]}...")
        print()
    except Exception as e:
        print(f"✗ Error: {e}\n")
    
    # Test 2: Non-existent file
    print("Test 2: Non-existent file")
    try:
        result = read_input_json("non_existent_file.json")
        print("✗ Should have failed!")
    except FileNotFoundError as e:
        print(f"✓ Correctly handled FileNotFoundError: {e}")
        print()
    except Exception as e:
        print(f"✗ Unexpected error: {e}\n")
    
    # Test 3: Invalid JSON
    print("Test 3: Invalid JSON file")
    # Create a file with invalid JSON
    with open("invalid.json", "w") as f:
        f.write('{"code_snippet": "test", "review_comments": [invalid json}')
    
    try:
        result = read_input_json("invalid.json")
        print("✗ Should have failed!")
    except json.JSONDecodeError as e:
        print(f"✓ Correctly handled JSONDecodeError")
        print()
    except Exception as e:
        print(f"✗ Unexpected error: {e}\n")
    finally:
        # Clean up
        if os.path.exists("invalid.json"):
            os.remove("invalid.json")
    
    # Test 4: Missing required keys
    print("Test 4: Missing required keys")
    # Create a file with missing keys
    with open("missing_keys.json", "w") as f:
        json.dump({"code_snippet": "test code"}, f)  # Missing review_comments
    
    try:
        result = read_input_json("missing_keys.json")
        print("✗ Should have failed!")
    except KeyError as e:
        print(f"✓ Correctly handled missing key: {e}")
        print()
    except Exception as e:
        print(f"✗ Unexpected error: {e}\n")
    finally:
        # Clean up
        if os.path.exists("missing_keys.json"):
            os.remove("missing_keys.json")
    
    # Test 5: Wrong data types
    print("Test 5: Wrong data types")
    # Create a file with wrong data types
    with open("wrong_types.json", "w") as f:
        json.dump({
            "code_snippet": 123,  # Should be string
            "review_comments": "not a list"  # Should be list
        }, f)
    
    try:
        result = read_input_json("wrong_types.json")
        print("✗ Should have failed!")
    except ValueError as e:
        print(f"✓ Correctly handled wrong data type: {e}")
        print()
    except Exception as e:
        print(f"✗ Unexpected error: {e}\n")
    finally:
        # Clean up
        if os.path.exists("wrong_types.json"):
            os.remove("wrong_types.json")
    
    print("All tests completed!")


if __name__ == "__main__":
    test_read_input_json()
