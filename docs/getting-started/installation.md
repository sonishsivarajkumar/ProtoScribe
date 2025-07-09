# Installation

This guide will help you install and set up ProtoScribe on your system.

## Prerequisites

Before installing ProtoScribe, ensure you have the following:

- **Python 3.10 or higher** - [Download Python](https://python.org/downloads/)
- **Node.js 18+ and npm** - [Download Node.js](https://nodejs.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads/)

!!! tip "Environment Check"
    You can verify your installations with:
    ```bash
    python --version    # Should show 3.10+
    node --version      # Should show 18+
    npm --version       # Should show recent version
    git --version       # Should show recent version
    ```

## Installation Methods

=== "Development Setup"

    ### 1. Clone the Repository
    
    ```bash
    git clone https://github.com/sonishsivarajkumar/ProtoScribe.git
    cd ProtoScribe
    ```
    
    ### 2. Backend Setup
    
    ```bash
    # Create virtual environment
    python -m venv .venv
    
    # Activate virtual environment
    # On macOS/Linux:
    source .venv/bin/activate
    # On Windows:
    .venv\Scripts\activate
    
    # Install dependencies
    pip install -e .
    ```
    
    ### 3. Frontend Setup
    
    ```bash
    # Navigate to frontend directory
    cd frontend
    
    # Install dependencies
    npm install
    
    # Return to project root
    cd ..
    ```

=== "Docker Setup"

    ### 1. Clone Repository
    
    ```bash
    git clone https://github.com/sonishsivarajkumar/ProtoScribe.git
    cd ProtoScribe
    ```
    
    ### 2. Build and Run with Docker Compose
    
    ```bash
    # Build and start all services
    docker-compose up --build
    ```
    
    This will start:
    - Backend API on `http://localhost:8000`
    - Frontend on `http://localhost:3000`
    - Database (if configured)

=== "Production Deployment"

    ### 1. Server Requirements
    
    - **CPU**: 2+ cores recommended
    - **RAM**: 4GB minimum, 8GB recommended
    - **Storage**: 10GB+ available space
    - **OS**: Linux (Ubuntu 20.04+ recommended)
    
    ### 2. Install Dependencies
    
    ```bash
    # Update system
    sudo apt update && sudo apt upgrade -y
    
    # Install Python 3.10+
    sudo apt install python3.10 python3.10-venv python3-pip -y
    
    # Install Node.js 18+
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
    
    # Install additional tools
    sudo apt install git nginx supervisor -y
    ```
    
    ### 3. Application Setup
    
    ```bash
    # Clone and setup application
    git clone https://github.com/sonishsivarajkumar/ProtoScribe.git
    cd ProtoScribe
    
    # Backend setup
    python3.10 -m venv .venv
    source .venv/bin/activate
    pip install -e .
    
    # Frontend setup
    cd frontend
    npm install
    npm run build
    cd ..
    ```

## Verification

After installation, verify everything is working:

### 1. Backend Verification

```bash
# Start the backend server
python start_backend.py
```

You should see output similar to:
```
Starting ProtoScribe Backend Server...
Visit http://localhost:8000/docs for API documentation
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Open http://localhost:8000/docs to see the API documentation.

### 2. Frontend Verification

```bash
# In a new terminal, navigate to frontend
cd frontend

# Start the frontend development server
npm run dev
```

You should see:
```
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

Open http://localhost:3000 to see the application interface.

## Common Issues

### Python Version Issues

!!! warning "Python Version"
    ProtoScribe requires Python 3.10 or higher. If you have an older version:
    
    **macOS (using Homebrew):**
    ```bash
    brew install python@3.10
    ```
    
    **Ubuntu/Debian:**
    ```bash
    sudo apt install python3.10 python3.10-venv
    ```
    
    **Windows:**
    Download from [python.org](https://python.org/downloads/)

### Node.js Issues

!!! warning "Node.js Version"
    The frontend requires Node.js 18 or higher:
    
    ```bash
    # Check current version
    node --version
    
    # Install Node.js 18+ using nvm (recommended)
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    nvm install 18
    nvm use 18
    ```

### Virtual Environment Issues

If you encounter issues with the virtual environment:

```bash
# Remove existing virtual environment
rm -rf .venv

# Create new virtual environment with specific Python version
python3.10 -m venv .venv

# Activate and install
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

### Permission Issues

On macOS/Linux, you might need to adjust permissions:

```bash
# Make scripts executable
chmod +x start_backend.py

# Fix ownership if needed
sudo chown -R $USER:$USER .
```

## Next Steps

Once installation is complete:

1. **Configure the application** - See [Configuration Guide](configuration.md)
2. **Take the quick start tour** - See [Quick Start Guide](quick-start.md)
3. **Explore the features** - See [User Guide](../user-guide/overview.md)

## Getting Help

If you encounter issues during installation:

- Check our [FAQ section](../about/support.md#frequently-asked-questions)
- Search [existing issues](https://github.com/sonishsivarajkumar/ProtoScribe/issues)
- Create a [new issue](https://github.com/sonishsivarajkumar/ProtoScribe/issues/new) with details about your system and the error
