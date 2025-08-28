#!/usr/bin/env python3
"""
FastAPI Web Application for Empathetic Code Reviewer
A web interface to upload code and get empathetic feedback
"""

from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import json
import tempfile
import re
from pathlib import Path
from typing import List, Optional
import uvicorn
from dotenv import load_dotenv

# Load environment variables from parent directory
load_dotenv("../.env")

# Import our existing functions
from core.empathetic_code_reviewer import read_input_json, generate_ai_prompt, create_markdown_section
from core.save_markdown_report import save_markdown_report, generate_full_report

# Initialize FastAPI app
app = FastAPI(
    title="Empathetic Code Reviewer",
    description="Generate empathetic and constructive code reviews using AI",
    version="1.0.0"
)

# Setup templates and static files
templates = Jinja2Templates(directory="../templates")

def markdown_to_html(markdown_text):
    """Convert markdown text to HTML with proper formatting"""
    if not markdown_text:
        return ""
    
    html = markdown_text
    
    # Convert headers
    html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Convert bold text
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    
    # Convert code blocks
    html = re.sub(r'```python\n(.*?)\n```', r'<pre class="code-block"><code class="python">\1</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'```\n(.*?)\n```', r'<pre class="code-block"><code>\1</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'```(.*?)```', r'<pre class="code-block"><code>\1</code></pre>', html, flags=re.DOTALL)
    
    # Convert inline code
    html = re.sub(r'`(.*?)`', r'<code class="inline-code">\1</code>', html)
    
    # Convert bullet points
    html = re.sub(r'^\* (.*$)', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'^\- (.*$)', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # Wrap consecutive list items in <ul>
    html = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)
    html = re.sub(r'</ul>\s*<ul>', '', html)
    
    # Convert line breaks
    html = html.replace('\n\n', '</p><p>')
    html = html.replace('\n', '<br>')
    
    # Wrap in paragraphs
    html = f'<p>{html}</p>'
    
    # Clean up empty paragraphs
    html = re.sub(r'<p>\s*</p>', '', html)
    html = re.sub(r'<p>\s*(<h[1-6]>)', r'\1', html)
    html = re.sub(r'(</h[1-6]>)\s*</p>', r'\1', html)
    
    # Handle horizontal rules
    html = html.replace('---', '<hr>')
    
    return html

# Add the function to Jinja2 templates
templates.env.filters['markdown_to_html'] = markdown_to_html

# Create directories if they don't exist (relative to project root)
Path("../templates").mkdir(exist_ok=True)
Path("../static").mkdir(exist_ok=True)
Path("../uploads").mkdir(exist_ok=True)
Path("../reports").mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="../static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Homepage with code review form"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/review", response_class=HTMLResponse)
async def create_review(
    request: Request,
    code_snippet: str = Form(...),
    comments: str = Form(...)
):
    """Process code review and return results"""
    try:
        # Parse comments (one per line)
        comment_list = [comment.strip() for comment in comments.split('\n') if comment.strip()]
        
        if not comment_list:
            raise HTTPException(status_code=400, detail="Please provide at least one review comment")
        
        # Create review data
        review_data = {
            "code_snippet": code_snippet,
            "review_comments": comment_list
        }
        
        # Generate the full report
        markdown_report = generate_full_report(review_data)
        
        # Save report to file
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"../reports/code_review_{timestamp}.md"
        
        success = save_markdown_report(markdown_report, report_filename)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save report")
        
        return templates.TemplateResponse("results_new.html", {
            "request": request,
            "report": markdown_report,
            "filename": report_filename,
            "success": True,
            "comment_count": len(comment_list)
        })
        
    except Exception as e:
        return templates.TemplateResponse("results_new.html", {
            "request": request,
            "success": False,
            "error": str(e)
        })

@app.post("/upload", response_class=HTMLResponse)
async def upload_json(request: Request, file: UploadFile = File(...)):
    """Upload JSON file for code review"""
    print(f"📤 Upload request received: {file.filename}")
    try:
        if not file.filename or not file.filename.endswith('.json'):
            print(f"❌ Invalid file type: {file.filename}")
            raise HTTPException(status_code=400, detail="Please upload a JSON file")
        
        print(f"✅ Valid JSON file: {file.filename}")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.json') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        print(f"📁 Temporary file saved: {tmp_file_path}")
        
        try:
            # Read the JSON file
            review_data = read_input_json(tmp_file_path)
            print(f"📋 JSON data loaded successfully with {len(review_data['review_comments'])} comments")
            
            # Generate the full report (optimized version)
            print(f"🚀 Starting optimized report generation...")
            markdown_report = generate_full_report(review_data)
            print(f"📝 Report generated successfully ({len(markdown_report)} characters)")
            
            # Save report to file
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"../reports/code_review_{timestamp}.md"
            
            success = save_markdown_report(markdown_report, report_filename)
            
            if not success:
                raise HTTPException(status_code=500, detail="Failed to save report")
            
            print(f"✅ Upload processing completed successfully")
            print(f"🎉 Report saved as: {report_filename}")
            
            return templates.TemplateResponse("results_new.html", {
                "request": request,
                "report": markdown_report,
                "filename": report_filename,
                "success": True,
                "comment_count": len(review_data['review_comments']),
                "uploaded_file": file.filename,
                "generation_complete": True
            })
            
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
                print(f"🗑️ Temporary file cleaned up")
            
    except Exception as e:
        print(f"❌ Upload error: {str(e)}")
        return templates.TemplateResponse("results_new.html", {
            "request": request,
            "success": False,
            "error": str(e)
        })

@app.get("/download/{filename}")
async def download_report(filename: str):
    """Download generated report"""
    file_path = f"../reports/{filename}"
    if os.path.exists(file_path):
        return FileResponse(
            file_path, 
            media_type='text/markdown',
            filename=filename
        )
    else:
        raise HTTPException(status_code=404, detail="Report not found")

@app.get("/reports")
async def list_reports(request: Request):
    """List all generated reports"""
    reports_dir = Path("../reports")
    reports = []
    
    if reports_dir.exists():
        for report_file in reports_dir.glob("*.md"):
            stat = report_file.stat()
            reports.append({
                "name": report_file.name,
                "size": f"{stat.st_size / 1024:.1f} KB",
                "created": stat.st_ctime
            })
    
    # Sort by creation time (newest first)
    reports.sort(key=lambda x: x["created"], reverse=True)
    
    return templates.TemplateResponse("reports.html", {
        "request": request,
        "reports": reports
    })

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Empathetic Code Reviewer API is running"}

@app.get("/api/sample")
async def get_sample_data():
    """Get sample data for testing"""
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
    return sample_data

if __name__ == "__main__":
    # Check if GEMINI_API_KEY is set
    if not os.getenv('GEMINI_API_KEY'):
        print("⚠️  Warning: GEMINI_API_KEY not set. The app will use simulated responses.")
        print("To use real AI responses, set your API key:")
        print("export GEMINI_API_KEY='your_api_key_here'")
    
    print("🚀 Starting Empathetic Code Reviewer Web App...")
    print("📱 Open your browser to: http://localhost:8000")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
