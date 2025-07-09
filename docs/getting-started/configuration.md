# Configuration

This guide covers all configuration options available in ProtoScribe, from basic setup to advanced customization.

## Environment Configuration

ProtoScribe uses environment variables for configuration. Create a `.env` file in your project root:

```bash
cp .env.example .env
```

### Basic Configuration

```bash
# API Configuration
PROJECT_NAME=ProtoScribe
VERSION=0.1.0

# Database
DATABASE_URL=sqlite:///./protoscribe.db

# Security
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

### AI Provider Configuration

=== "OpenAI Setup"

    ```bash
    # OpenAI Configuration
    OPENAI_API_KEY=sk-your-openai-api-key-here
    DEFAULT_LLM_PROVIDER=openai
    DEFAULT_MODEL=gpt-4
    
    # Model Settings
    LLM_TEMPERATURE=0.3
    LLM_MAX_TOKENS=2000
    LLM_TIMEOUT=30
    ```
    
    **Getting Your OpenAI API Key:**
    
    1. Visit [OpenAI API](https://platform.openai.com/api-keys)
    2. Sign in or create an account
    3. Click "Create new secret key"
    4. Copy the key to your `.env` file
    
    !!! warning "Keep Your Key Secret"
        Never commit your API key to version control. The `.env` file is already in `.gitignore`.

=== "Anthropic Setup"

    ```bash
    # Anthropic Configuration
    ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
    DEFAULT_LLM_PROVIDER=anthropic
    DEFAULT_MODEL=claude-3-sonnet-20240229
    
    # Model Settings
    LLM_TEMPERATURE=0.3
    LLM_MAX_TOKENS=2000
    LLM_TIMEOUT=30
    ```
    
    **Getting Your Anthropic API Key:**
    
    1. Visit [Anthropic Console](https://console.anthropic.com/)
    2. Sign in or create an account
    3. Navigate to API Keys
    4. Generate a new key
    5. Copy the key to your `.env` file

=== "Multiple Providers"

    ```bash
    # Multiple Provider Configuration
    OPENAI_API_KEY=sk-your-openai-key
    ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
    DEFAULT_LLM_PROVIDER=openai
    
    # Provider Comparison Settings
    ENABLE_PROVIDER_COMPARISON=true
    MAX_PROVIDERS_PER_ANALYSIS=2
    ```

### Analysis Configuration

```bash
# AI Analysis Settings
MIN_CONFIDENCE_THRESHOLD=0.6
MAX_SUGGESTIONS_PER_ITEM=3
ENABLE_ADVANCED_ANALYSIS=true

# Performance Settings
ANALYSIS_TIMEOUT=300  # 5 minutes
CONCURRENT_ANALYSES=2
CACHE_ANALYSIS_RESULTS=true
```

### File Processing Configuration

```bash
# File Processing
MAX_FILE_SIZE=52428800  # 50MB
ALLOWED_FILE_TYPES=[".pdf", ".docx", ".txt"]
UPLOAD_DIR=uploads
TEMP_DIR=temp

# Document Processing
EXTRACT_IMAGES=false
OCR_ENABLED=false
LANGUAGE_DETECTION=true
```

## Advanced Configuration

### Database Configuration

=== "SQLite (Default)"

    ```bash
    DATABASE_URL=sqlite:///./protoscribe.db
    DB_ECHO=false  # Set to true for SQL logging
    ```

=== "PostgreSQL"

    ```bash
    # PostgreSQL Configuration
    DATABASE_URL=postgresql://user:password@localhost/protoscribe
    DB_POOL_SIZE=5
    DB_MAX_OVERFLOW=10
    DB_POOL_TIMEOUT=30
    ```
    
    **Setup PostgreSQL:**
    ```bash
    # Install PostgreSQL
    sudo apt install postgresql postgresql-contrib
    
    # Create database and user
    sudo -u postgres psql
    CREATE DATABASE protoscribe;
    CREATE USER protoscribe_user WITH PASSWORD 'your_password';
    GRANT ALL PRIVILEGES ON DATABASE protoscribe TO protoscribe_user;
    \q
    ```

=== "MySQL"

    ```bash
    # MySQL Configuration
    DATABASE_URL=mysql://user:password@localhost/protoscribe
    DB_POOL_SIZE=5
    DB_MAX_OVERFLOW=10
    ```

### Logging Configuration

```bash
# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/protoscribe.log
LOG_ROTATION=daily
LOG_MAX_SIZE=100MB
LOG_BACKUP_COUNT=7

# Specific Logger Levels
UVICORN_LOG_LEVEL=INFO
SQLALCHEMY_LOG_LEVEL=WARNING
HTTPX_LOG_LEVEL=WARNING
```

### Security Configuration

```bash
# Security Settings
SECRET_KEY=your-very-long-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Password Requirements
MIN_PASSWORD_LENGTH=8
REQUIRE_UPPERCASE=true
REQUIRE_LOWERCASE=true
REQUIRE_NUMBERS=true
REQUIRE_SYMBOLS=true

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600  # 1 hour

# CORS Settings
ALLOWED_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
ALLOWED_METHODS=["GET", "POST", "PUT", "DELETE"]
ALLOWED_HEADERS=["*"]
```

## Frontend Configuration

### Next.js Configuration

Create `frontend/.env.local`:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_NAME=ProtoScribe
NEXT_PUBLIC_APP_VERSION=0.1.0

# Features
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_SENTRY=false

# UI Settings
NEXT_PUBLIC_THEME=light
NEXT_PUBLIC_DEFAULT_LOCALE=en
```

### Build Configuration

Update `frontend/next.config.js`:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  trailingSlash: true,
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ]
  },
}

module.exports = nextConfig
```

## Configuration Validation

ProtoScribe validates configuration on startup. You can test your configuration:

```bash
# Validate backend configuration
python -c "from src.protoscribe.core.config import settings; print('✅ Configuration valid')"

# Test AI provider connections
python -c "
from src.protoscribe.services.advanced_llm_analyzer import AdvancedLLMAnalyzer
analyzer = AdvancedLLMAnalyzer()
print(f'✅ AI Provider: {analyzer.provider}')
"
```

## Environment-Specific Configurations

### Development

```bash
# .env.development
DEBUG=true
LOG_LEVEL=DEBUG
RELOAD=true
CORS_ALLOW_ALL=true

# Development AI Settings
USE_MOCK_AI=true  # Use mock responses when API keys not available
CACHE_AI_RESPONSES=true
```

### Production

```bash
# .env.production
DEBUG=false
LOG_LEVEL=INFO
RELOAD=false

# Production Security
SECRET_KEY=your-production-secret-key
CORS_ALLOW_ALL=false
ALLOWED_ORIGINS=["https://yourdomain.com"]

# Production Database
DATABASE_URL=postgresql://user:pass@prod-db:5432/protoscribe

# Performance
WORKERS=4
MAX_CONNECTIONS=100
```

### Testing

```bash
# .env.testing
DATABASE_URL=sqlite:///./test.db
LOG_LEVEL=WARNING
USE_MOCK_AI=true
DISABLE_AUTH=true  # For testing purposes
```

## Configuration Reference

### Complete Settings List

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `PROJECT_NAME` | string | "ProtoScribe" | Application name |
| `VERSION` | string | "0.1.0" | Application version |
| `DEBUG` | boolean | false | Enable debug mode |
| `DATABASE_URL` | string | sqlite:///./protoscribe.db | Database connection |
| `SECRET_KEY` | string | - | JWT signing key |
| `OPENAI_API_KEY` | string | - | OpenAI API key |
| `ANTHROPIC_API_KEY` | string | - | Anthropic API key |
| `DEFAULT_LLM_PROVIDER` | string | "openai" | Default AI provider |
| `LLM_TEMPERATURE` | float | 0.3 | AI creativity level |
| `LLM_MAX_TOKENS` | integer | 2000 | Maximum AI response length |
| `MAX_FILE_SIZE` | integer | 52428800 | Maximum upload size (bytes) |
| `LOG_LEVEL` | string | "INFO" | Logging verbosity |

### Validation Rules

ProtoScribe validates configuration using Pydantic:

```python
from pydantic import validator

class Settings(BaseSettings):
    @validator('LLM_TEMPERATURE')
    def validate_temperature(cls, v):
        if not 0 <= v <= 2:
            raise ValueError('Temperature must be between 0 and 2')
        return v
    
    @validator('MAX_FILE_SIZE')
    def validate_file_size(cls, v):
        if v > 100 * 1024 * 1024:  # 100MB
            raise ValueError('File size too large')
        return v
```

## Troubleshooting Configuration

### Common Issues

!!! warning "Invalid API Key"
    ```
    Error: Invalid OpenAI API key
    ```
    **Solution**: Check your API key format and ensure it has the correct permissions.

!!! warning "Database Connection Failed"
    ```
    Error: Could not connect to database
    ```
    **Solution**: Verify your `DATABASE_URL` format and database server is running.

!!! warning "CORS Error"
    ```
    Error: CORS policy blocked
    ```
    **Solution**: Add your frontend URL to `ALLOWED_ORIGINS` in the backend configuration.

### Configuration Testing

Test specific configuration aspects:

```bash
# Test database connection
python -c "from src.protoscribe.models.database import engine; engine.connect(); print('✅ Database OK')"

# Test AI provider
python -c "
import os
if os.getenv('OPENAI_API_KEY'):
    print('✅ OpenAI key configured')
if os.getenv('ANTHROPIC_API_KEY'):
    print('✅ Anthropic key configured')
"

# Test file permissions
python -c "
import os
upload_dir = os.getenv('UPLOAD_DIR', 'uploads')
os.makedirs(upload_dir, exist_ok=True)
print(f'✅ Upload directory: {upload_dir}')
"
```

## Next Steps

After configuring ProtoScribe:

1. **Test your setup** - Run the [Quick Start Guide](quick-start.md)
2. **Explore features** - See [User Guide](../user-guide/overview.md)
3. **Customize further** - Check [Developer Guide](../developer-guide/architecture.md)
