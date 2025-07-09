# ProtoScribe - Trial Protocol AI Optimizer

Clinical trial protocols are lengthy, complex documents that must adhere to CONSORT/SPIRIT guidelines. Manual compliance checking is time-consuming and error-prone. The Trial Protocol AI Optimizer accelerates and standardizes protocol drafting by automatically identifying missing or under-specified elements and suggesting high-quality text.

## Features

- **Document Ingestion**: Accepts PDF, DOCX, or plain-text protocols via drag-and-drop or file dialog
- **Section Segmentation**: Identifies major headings and builds structured document tree
- **Compliance Checking**: Validates against CONSORT/SPIRIT guidelines
- **LLM-Powered Analysis**: Uses AI to identify missing or incomplete elements
- **Interactive Review UI**: Side-by-side comparison with accept/edit/reject workflow
- **Protocol Scoring**: Computes completeness scores and generates reports
- **Version Control**: Tracks edits and maintains revision history
- **Export & Integration**: Outputs to DOCX/PDF with optional API integrations

## Quick Start

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
- [ ] File ingestion (PDF, DOCX, text)
- [ ] Section segmentation and parsing
- [ ] Basic rule-based compliance checking
- [ ] Scoring system

### Phase 2: AI Integration
- [ ] LLM integration with LangChain
- [ ] Missing item detection
- [ ] Suggestion generation
- [ ] Prompt templates for guidelines

### Phase 3: Interactive UI
- [ ] React frontend with Tailwind CSS
- [ ] Side-by-side editor interface
- [ ] Accept/edit/reject workflow
- [ ] Version history and comparison

### Phase 4: Advanced Features
- [ ] Export templates (DOCX/PDF)
- [ ] API integrations
- [ ] Team collaboration
- [ ] Advanced analytics

## Contributing

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

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Citation

If you use ProtoScribe in your research, please cite:

```bibtex
@software{protoscribe,
  title={ProtoScribe: Clinical Trial Protocol AI Optimizer},
  author={Sivarajkumar, Sonish},
  year={2025},
  url={https://github.com/sonishsivarajkumar/ProtoScribe}
}
```

## Support

- Documentation: https://protoscribe.readthedocs.io
- Issues: https://github.com/sonishsivarajkumar/ProtoScribe/issues
- Discussions: https://github.com/sonishsivarajkumar/ProtoScribe/discussions
