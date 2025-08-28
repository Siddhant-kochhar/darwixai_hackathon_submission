#!/usr/bin/env python3
"""
Empathetic Code Reviewer - Entry Point
Run this script to start the web application
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Add src directory to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

if __name__ == "__main__":
    try:
        import uvicorn
        
        # Check if GEMINI_API_KEY is set
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("⚠️  Warning: GEMINI_API_KEY not set. The app will use simulated responses.")
            print("To use real AI responses, set your API key:")
            print("export GEMINI_API_KEY='your_api_key_here'")
        else:
            print("✅ GEMINI_API_KEY loaded successfully!")
            print("🤖 Real AI responses enabled!")
        
        print("🚀 Starting Empathetic Code Reviewer Web App...")
        print("📱 Open your browser to: http://localhost:8000")
        print("🔥 Project created by Siddhant Kochhar")
        print("📧 Contact: siddhant.kochhar1@gmail.com")
        
        # Change to src directory and run with import string
        os.chdir(src_path)
        uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
        
    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("Make sure you have installed dependencies:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)
