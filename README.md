<div align="center">

# 🧬 ProtoScribe
### *Clinical Trial Protocol AI Optimizer*

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)](https://nextjs.org/)
[![Documentation](https://img.shields.io/badge/docs-MkDocs-blue.svg)](https://sonishsivarajkumar.github.io/ProtoScribe)

*Accelerate clinical trial protocol development with AI-powered compliance checking and intelligent suggestions*

[**📖 Documentation**](https://sonishsivarajkumar.github.io/ProtoScribe) • [**🚀 Quick Start**](#-quick-start) • [**🔧 API Reference**](https://sonishsivarajkumar.github.io/ProtoScribe/api-reference/overview/) • [**💬 Discussions**](https://github.com/sonishsivarajkumar/ProtoScribe/discussions)

</div>

---

## 🎯 Overview

Clinical trial protocols are complex documents that must adhere to **CONSORT/SPIRIT guidelines**. Manual compliance checking is time-consuming and error-prone. ProtoScribe transforms protocol development by:

- **🤖 AI-Powered Analysis** - Automatically identifies missing or under-specified elements
- **📊 Real-time Compliance** - Validates against international guidelines  
- **✨ Smart Suggestions** - Generates high-quality text improvements
- **⚡ Interactive Workflow** - Streamlined review and editing interface

## 🌟 Features

<table>
<tr>
<td width="50%">

### 📄 **Document Processing**
- **Multi-format Support** - PDF, DOCX, plain text
- **Smart Segmentation** - Automatic section detection
- **Structure Analysis** - Document tree generation

### 🔍 **AI Analysis**
- **Compliance Validation** - CONSORT/SPIRIT guidelines
- **Missing Element Detection** - Comprehensive scanning
- **Intelligent Suggestions** - Context-aware improvements

</td>
<td width="50%">

### 🎛️ **Interactive Interface**
- **Side-by-side Editor** - Compare original and suggestions
- **Review Workflow** - Accept, edit, or reject changes
- **Real-time Scoring** - Protocol completeness metrics

### 📊 **Export & Integration**
- **Multiple Formats** - DOCX, PDF export
- **Version Control** - Track changes and history
- **API Integration** - Programmatic access

</td>
</tr>
</table>

## 🚀 Quick Start

### Prerequisites

<table>
<tr>
<td><strong>🐍 Python</strong></td>
<td>3.10+ required</td>
</tr>
<tr>
<td><strong>🟢 Node.js</strong></td>
<td>18+ for frontend</td>
</tr>
<tr>
<td><strong>🔑 API Keys</strong></td>
<td>OpenAI or Anthropic</td>
</tr>
</table>

### Installation

```bash
# Clone the repository
git clone https://github.com/sonishsivarajkumar/ProtoScribe.git
cd ProtoScribe

# Install dependencies
pip install -e .

# Install development dependencies
pip install -e ".[dev]"

# Download spaCy language model
python -m spacy download en_core_web_sm
```

### Configuration

Create a `.env` file in the project root:

```env
# LLM API Configuration
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///./protoscribe.db

# Security
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Running the Application

```bash
# Start the backend server
uvicorn src.protoscribe.main:app --reload

# The API will be available at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

### Frontend Development

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Frontend will be available at http://localhost:3000
```

## Project Structure

```
protoscribe/
├── src/
│   └── protoscribe/
│       ├── api/              # FastAPI endpoints
│       ├── core/             # Core business logic
│       ├── models/           # Database models
│       ├── services/         # Service layer
│       └── utils/            # Utility functions
├── frontend/                 # React frontend
├── guidelines/               # CONSORT/SPIRIT knowledge base
├── tests/                    # Test suite
├── docs/                     # Documentation
└── scripts/                  # Utility scripts
```

## Development Roadmap

### Phase 1: Foundation (MVP)
- [x] Project setup and structure
- [x] FastAPI backend with LLM integration
- [x] React frontend with Tailwind CSS
- [x] Database models and API endpoints
- [x] Basic compliance checking framework

### Phase 2: AI Integration
- [x] LLM integration (OpenAI/Anthropic)
- [x] Advanced prompt templates
- [x] Provider comparison and fallback
- [x] Suggestion generation pipeline

### Phase 3: Interactive UI
- [x] Side-by-side editor interface
- [x] Accept/edit/reject workflow
- [x] Real-time protocol scoring
- [x] Executive summary generation

### Phase 4: Advanced Features
- [ ] Export templates (DOCX/PDF)
- [ ] Advanced analytics dashboard
- [ ] Team collaboration features
- [ ] Production database integration

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Format code
black src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/
```

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 📚 Citation

If you use ProtoScribe in your research, please cite:

```bibtex
@software{protoscribe,
  title={ProtoScribe: Clinical Trial Protocol AI Optimizer},
  author={Sivarajkumar, Sonish},
  year={2025},
  url={https://github.com/sonishsivarajkumar/ProtoScribe}
}
```

## 🆘 Support

- **📖 Documentation**: https://sonishsivarajkumar.github.io/ProtoScribe
- **🐛 Issues**: https://github.com/sonishsivarajkumar/ProtoScribe/issues
- **💬 Discussions**: https://github.com/sonishsivarajkumar/ProtoScribe/discussions

---

<div align="center">

**[⭐ Star this repository](https://github.com/sonishsivarajkumar/ProtoScribe) if you find it helpful!**

Made with ❤️ by [Sonish Sivarajkumar](https://github.com/sonishsivarajkumar)

</div>
