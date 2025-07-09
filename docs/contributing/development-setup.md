# Development Setup

Get your development environment ready to contribute to ProtoScribe! This guide covers everything from initial setup to running tests.

## Prerequisites

### Required Software

- **Python 3.11+**: Main backend language
- **Node.js 18+**: Frontend development
- **Git**: Version control
- **VS Code** (recommended): IDE with excellent Python and TypeScript support

### Optional but Recommended

- **Docker**: For containerized development
- **Redis**: For caching (can use Docker)
- **PostgreSQL**: For production-like database testing

## Quick Setup

### 1. Clone the Repository

```bash
git clone https://github.com/sonishsivarajkumar/ProtoScribe.git
cd ProtoScribe
```

### 2. Backend Setup

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### 3. Frontend Setup

```bash
cd frontend
npm install
cd ..
```

### 4. Initialize Database

```bash
# Run database migrations
python -m alembic upgrade head

# Optional: Load sample data
python scripts/load_sample_data.py
```

### 5. Verify Setup

```bash
# Start backend (terminal 1)
python run.py

# Start frontend (terminal 2)
cd frontend && npm run dev

# Run tests (terminal 3)
pytest
```

You should see:
- Backend API at http://localhost:8000
- Frontend app at http://localhost:3000
- Interactive API docs at http://localhost:8000/docs

## Detailed Setup Guide

### Python Environment

#### Using Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate (Linux/Mac)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Verify activation
which python  # Should show path to .venv/bin/python
```

#### Using Conda
```bash
# Create conda environment
conda create -n protoscribe python=3.11
conda activate protoscribe

# Install pip packages
pip install -e .
```

### Environment Configuration

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
# Database
DATABASE_URL=sqlite:///./protoscribe.db

# AI Providers (optional for development)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Development settings
DEBUG=true
LOG_LEVEL=INFO

# Frontend URL
FRONTEND_URL=http://localhost:3000

# File storage
UPLOAD_DIR=./storage/uploads
MAX_FILE_SIZE=52428800  # 50MB in bytes
```

### Database Setup

#### SQLite (Development)
```bash
# Initialize database
python -c "from src.protoscribe.core.database import init_db; init_db()"

# Run migrations
python -m alembic upgrade head
```

#### PostgreSQL (Production-like)
```bash
# Start PostgreSQL with Docker
docker run --name protoscribe-postgres \
  -e POSTGRES_DB=protoscribe \
  -e POSTGRES_USER=protoscribe \
  -e POSTGRES_PASSWORD=protoscribe \
  -p 5432:5432 \
  -d postgres:15

# Update .env
DATABASE_URL=postgresql://protoscribe:protoscribe@localhost:5432/protoscribe

# Run migrations
python -m alembic upgrade head
```

### Frontend Dependencies

```bash
cd frontend

# Install dependencies
npm install

# Install additional development tools
npm install -D @types/node @types/react @types/react-dom

# Verify setup
npm run build
npm run dev
```

## Development Workflow

### Running the Application

#### Option 1: Individual Components
```bash
# Terminal 1: Backend
cd /path/to/protoscribe
source .venv/bin/activate
python run.py

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Documentation (optional)
mkdocs serve
```

#### Option 2: Using Docker Compose
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Making Changes

#### Backend Changes
1. **Code Changes**: Edit files in `src/protoscribe/`
2. **Database Changes**: Create migration with `alembic revision --autogenerate -m "description"`
3. **Dependencies**: Update `pyproject.toml` and run `pip install -e .`
4. **Testing**: Run `pytest` to ensure changes work

#### Frontend Changes
1. **Code Changes**: Edit files in `frontend/`
2. **Dependencies**: Update `package.json` and run `npm install`
3. **Building**: Run `npm run build` to check for build errors
4. **Testing**: Run `npm test` (when tests are available)

#### Documentation Changes
1. **Edit Docs**: Update files in `docs/`
2. **Local Preview**: Run `mkdocs serve`
3. **Build Check**: Run `mkdocs build`

### Common Development Tasks

#### Adding a New API Endpoint
```bash
# 1. Create endpoint in appropriate router
# src/protoscribe/api/routes.py or create new router file

# 2. Add data models if needed
# src/protoscribe/models/database.py

# 3. Create database migration if schema changed
alembic revision --autogenerate -m "Add new endpoint models"
alembic upgrade head

# 4. Add tests
# tests/api/test_new_endpoint.py

# 5. Update documentation
# docs/api-reference/new-endpoint.md
```

#### Adding a New Frontend Component
```bash
# 1. Create component
# frontend/components/new-component/NewComponent.tsx

# 2. Add types if needed
# frontend/lib/types.ts

# 3. Update API client if needed
# frontend/lib/api.ts

# 4. Add to page or parent component
# frontend/app/page.tsx or appropriate page

# 5. Test in browser
npm run dev
```

## IDE Configuration

### VS Code Setup

Recommended extensions:
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.pylint",
    "ms-python.black-formatter",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-typescript-next"
  ]
}
```

Settings (`.vscode/settings.json`):
```json
{
  "python.defaultInterpreterPath": "./.venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "typescript.preferences.importModuleSpecifier": "relative"
}
```

### PyCharm Setup

1. **Open Project**: Open the ProtoScribe directory
2. **Interpreter**: Set Python interpreter to `.venv/bin/python`
3. **Code Style**: Import code style from `.editorconfig`
4. **Run Configurations**: 
   - Backend: `python run.py`
   - Tests: `pytest`

## Troubleshooting

### Common Issues

#### Python Virtual Environment
```bash
# Issue: Command not found after activation
# Solution: Check if activation worked
which python
echo $VIRTUAL_ENV

# Issue: Package installation fails
# Solution: Update pip
pip install --upgrade pip
```

#### Database Issues
```bash
# Issue: Migration fails
# Solution: Reset database (development only)
rm protoscribe.db
alembic stamp head
alembic upgrade head

# Issue: Connection error
# Solution: Check database is running
python -c "from src.protoscribe.core.database import check_db_health; print(check_db_health())"
```

#### Frontend Issues
```bash
# Issue: npm install fails
# Solution: Clear cache and reinstall
rm -rf node_modules package-lock.json
npm cache clean --force
npm install

# Issue: TypeScript errors
# Solution: Check TypeScript version and configuration
npx tsc --version
npx tsc --noEmit
```

#### API Connection Issues
```bash
# Issue: Frontend can't connect to backend
# Solution: Check CORS settings and URLs
curl http://localhost:8000/api/protocols/
# Should return JSON response

# Check .env configuration
cat .env | grep -E "(API_URL|FRONTEND_URL)"
```

### Environment Issues

#### Port Conflicts
```bash
# Find process using port 8000
lsof -i :8000
# Kill process if needed
kill -9 <PID>

# Use different port
export PORT=8001
python run.py
```

#### Permission Issues
```bash
# Fix file permissions
chmod +x scripts/*.py
chmod +x run.py

# Fix directory permissions
chmod -R 755 storage/
```

### Performance Issues

#### Slow API Responses
```bash
# Enable debug mode
export DEBUG=true
export LOG_LEVEL=DEBUG
python run.py

# Check logs for slow queries
tail -f logs/protoscribe.log
```

#### Large File Uploads
```bash
# Increase upload limits (development only)
export MAX_FILE_SIZE=104857600  # 100MB
```

## Development Tools

### Code Quality

#### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

#### Code Formatting
```bash
# Python formatting
black src/ tests/
isort src/ tests/

# Frontend formatting
cd frontend
npx prettier --write .
```

#### Linting
```bash
# Python linting
pylint src/
mypy src/

# Frontend linting
cd frontend
npm run lint
```

### Testing

#### Backend Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/protoscribe

# Run specific test file
pytest tests/api/test_protocols.py

# Run with debug output
pytest -v -s
```

#### Frontend Tests
```bash
cd frontend

# Run tests (when available)
npm test

# Run with coverage
npm run test:coverage
```

### Database Tools

#### Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Check migration status
alembic current
alembic history
```

#### Database Inspection
```bash
# SQLite inspection
sqlite3 protoscribe.db ".schema"
sqlite3 protoscribe.db "SELECT * FROM protocols LIMIT 5;"

# PostgreSQL inspection
psql postgresql://protoscribe:protoscribe@localhost:5432/protoscribe
\dt  -- List tables
\d protocols  -- Describe table
```

## Contributing Checklist

Before submitting a pull request:

- [ ] Code follows project style guidelines
- [ ] All tests pass (`pytest` and `npm test`)
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Migration created if database schema changed
- [ ] `.env.example` updated if new environment variables added
- [ ] No sensitive information in code or comments
- [ ] Code is properly commented
- [ ] Git commit messages are descriptive

## Getting Help

### Documentation
- **API Docs**: http://localhost:8000/docs (when backend is running)
- **Project Docs**: http://localhost:8001 (when `mkdocs serve` is running)
- **README**: Check the main README.md for quick reference

### Community
- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and ideas
- **Code Review**: Submit PRs for feedback

### Debugging
- **Backend Logs**: Check console output or log files
- **Frontend Logs**: Check browser developer console
- **Database Logs**: Check database connection and query logs
- **API Testing**: Use http://localhost:8000/docs for interactive testing

!!! tip "Development Tip"
    Start with small changes and test frequently. The development setup is designed for rapid iteration and testing.

!!! warning "Database Changes"
    Always create migrations for database schema changes, even in development. This ensures consistency across all environments.

!!! info "Performance"
    The development setup prioritizes ease of use over performance. For production-like performance testing, use the Docker setup with PostgreSQL.
