# 🤖 Empathetic Code Reviewer

> **Transforming Critical Feedback into Constructive Growth**

A sophisticated web application that leverages AI to transform harsh code review comments into empathetic, constructive feedback that helps developers learn and grow.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0+-green.svg)](https://fastapi.tiangolo.com/)
[![Google Gemini AI](https://img.shields.io/badge/AI-Google%20Gemini-orange.svg)](https://ai.google.dev/)

## 🌟 Features

- **🎯 Empathetic Feedback**: Transforms critical comments into encouraging, constructive guidance
- **⚡ Fast Processing**: Optimized concurrent AI processing for multiple comments
- **📱 Modern Web UI**: Clean, responsive interface with real-time feedback
- **📄 Multiple Input Methods**: Upload JSON files or input code manually
- **📊 Professional Reports**: Generate downloadable Markdown reports
- **🚀 AI-Powered**: Uses Google Gemini AI for intelligent analysis

## 🏗️ Architecture

```
project_reviewer/
├── src/
│   ├── core/                     # Core business logic
│   │   ├── empathetic_code_reviewer.py
│   │   └── save_markdown_report.py
│   └── app.py                    # FastAPI web application
├── templates/                    # HTML templates
│   ├── index.html
│   ├── results_new.html
│   └── reports.html
├── static/                       # Static assets
├── tests/                        # Unit tests
├── examples/                     # Sample JSON files
├── docs/                         # Documentation
├── reports/                      # Generated reports
└── requirements.txt              # Dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd project_reviewer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file and add your GEMINI_API_KEY
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   cd src
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8000`

## 📖 Usage

### Method 1: Web Interface (Recommended)

1. Open `http://localhost:8000` in your browser
2. Choose between **Manual Input** or **Upload JSON** tabs
3. For manual input:
   - Paste your code snippet
   - Add review comments (one per line)
   - Click "Generate Review"
4. For file upload:
   - Upload a JSON file with the required format
   - Click "Upload & Review"

### Method 2: JSON File Upload

Create a JSON file with this structure:

```json
{
  "code_snippet": "def calculate_area(radius):\n    return 3.14 * radius * radius",
  "review_comments": [
    "Consider using math.pi instead of hardcoded 3.14",
    "Add input validation for the radius parameter",
    "Include error handling for negative values"
  ]
}
```

## 🎯 API Endpoints

- `GET /` - Main application interface
- `POST /review` - Process manual code review
- `POST /upload` - Upload JSON file for review
- `GET /reports` - List all generated reports
- `GET /download/{filename}` - Download specific report
- `GET /api/health` - Health check endpoint
- `GET /api/sample` - Get sample JSON data

## 🧪 Testing

Run the test suite:

```bash
cd tests
python -m pytest
```

## 📊 Performance Optimizations

- **Concurrent Processing**: Multiple AI requests processed in parallel
- **Optimized Prompts**: Shorter, more efficient prompts for faster responses
- **Token Limits**: Controlled output length for consistent performance
- **Timeout Protection**: 30-second timeout per comment processing
- **Resource Management**: Efficient memory and API usage

## 🛠️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### Model Settings

The application uses optimized Google Gemini settings:
- Model: `gemini-1.5-flash`
- Temperature: 0.7
- Max Tokens: 800
- Concurrent Workers: 3

## 📈 Example Output

The application generates empathetic reports with:

- **Positive Rephrasing**: Encouraging version of critical feedback
- **Technical Explanation**: Clear reasoning behind suggestions
- **Code Examples**: Practical implementation guidance
- **Holistic Summary**: Overall encouragement and growth focus

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

**Siddhant Kochhar**

- 📧 Email: [siddhant.kochhar1@gmail.com](mailto:siddhant.kochhar1@gmail.com)
- 💼 LinkedIn: [linkedin.com/in/siddhant-kochhar](https://www.linkedin.com/in/siddhant-kochhar)
- 📱 Contact: [+91 8965897560](tel:+918965897560)

---

<div align="center">

**🚀 Transforming Critical Feedback into Constructive Growth**

*Built with ❤️ using FastAPI & Google Gemini AI*

</div>
