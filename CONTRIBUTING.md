# Contributing to ProtoScribe

Thank you for your interest in contributing to ProtoScribe! This document provides guidelines for contributing to the Clinical Trial Protocol AI Optimizer.

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- Node.js 18+ (for frontend development)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/sonishsivarajkumar/ProtoScribe.git
   cd ProtoScribe
   ```

2. **Run the setup script**
   ```bash
   python run.py
   ```
   Choose option 1 for quick start.

3. **Manual setup (alternative)**
   ```bash
   # Install dependencies
   pip install -e .
   pip install -e ".[dev]"
   
   # Download spaCy model
   python -m spacy download en_core_web_sm
   
   # Copy environment file
   cp .env.example .env
   
   # Edit .env to add your API keys
   ```

## Development Workflow

### Code Style

We use the following tools for code quality:

- **Black** for code formatting
- **flake8** for linting  
- **mypy** for type checking
- **pytest** for testing

Run all checks:
```bash
python scripts/run_tests.py
```

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Write code and tests**
   - Add tests for new functionality
   - Update documentation as needed
   - Follow existing code patterns

3. **Run tests**
   ```bash
   pytest tests/ -v
   ```

4. **Format code**
   ```bash
   black src/ tests/
   flake8 src/ tests/
   mypy src/
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   git push origin feature/your-feature-name
   ```

6. **Create pull request**

### Testing

#### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/protoscribe

# Run specific test file
pytest tests/test_document_processor.py

# Run with verbose output
pytest -v
```

#### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names
- Include both positive and negative test cases
- Mock external dependencies (APIs, file system)

Example test:
```python
import pytest
from src.protoscribe.services.document_processor import DocumentProcessor

class TestDocumentProcessor:
    def setup_method(self):
        self.processor = DocumentProcessor()
    
    @pytest.mark.asyncio
    async def test_process_document(self, temp_file):
        result = await self.processor.process_document(temp_file)
        assert result is not None
        assert "title" in result
```

## Project Structure

```
protoscribe/
├── src/protoscribe/           # Main application
│   ├── api/                   # FastAPI routes
│   ├── core/                  # Configuration
│   ├── models/                # Database models
│   ├── services/              # Business logic
│   └── utils/                 # Utility functions
├── guidelines/                # CONSORT/SPIRIT data
├── tests/                     # Test suite
├── frontend/                  # React frontend
├── scripts/                   # Development tools
└── docs/                      # Documentation
```

## Guidelines Knowledge Base

### Adding New Guidelines

1. Create JSON file in `guidelines/` directory
2. Follow the existing structure:
   ```json
   {
     "name": "GUIDELINE_NAME",
     "version": "2023",
     "description": "Description",
     "items": [
       {
         "id": "1a",
         "section": "Section Name",
         "description": "Item description",
         "keywords": ["keyword1", "keyword2"]
       }
     ]
   }
   ```

3. Update the compliance checker to load the new guideline
4. Add tests for the new guideline

### Updating Existing Guidelines

- Maintain backward compatibility
- Update version numbers
- Document changes in commit messages

## API Development

### Adding New Endpoints

1. Create route in appropriate module under `src/protoscribe/api/`
2. Add request/response models in `src/protoscribe/models/`
3. Implement business logic in `src/protoscribe/services/`
4. Add comprehensive tests
5. Update API documentation

### API Design Principles

- Use RESTful conventions
- Include proper HTTP status codes
- Provide detailed error messages
- Use Pydantic models for validation
- Add OpenAPI documentation

## Frontend Development

### Setup

```bash
cd frontend
npm install
npm run dev
```

### Guidelines

- Use TypeScript for type safety
- Follow React best practices
- Use Tailwind CSS for styling
- Implement responsive design
- Add accessibility features

## Documentation

### Types of Documentation

1. **Code comments** - Explain complex logic
2. **Docstrings** - Document functions and classes
3. **README** - Project overview and setup
4. **API docs** - Automatic via FastAPI
5. **User guides** - Usage instructions

### Writing Good Documentation

- Be clear and concise
- Include examples
- Keep documentation up to date
- Use proper markdown formatting

## Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- Major: Breaking changes
- Minor: New features
- Patch: Bug fixes

### Release Checklist

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Run full test suite
4. Create release tag
5. Build and publish package
6. Update documentation

## Getting Help

### Resources

- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - General questions and ideas
- **Documentation** - Comprehensive guides
- **Code Examples** - Check the test suite

### Reporting Issues

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages and stack traces

### Requesting Features

For feature requests, please:
- Describe the use case
- Explain the expected behavior
- Consider implementation challenges
- Discuss alternatives

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain professional communication

### Unacceptable Behavior

- Harassment or discrimination
- Offensive language or content
- Personal attacks
- Spam or off-topic discussions

## License

ProtoScribe is licensed under the Apache License 2.0. By contributing, you agree that your contributions will be licensed under the same license.

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to ProtoScribe! 🎉
