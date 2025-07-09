#!/usr/bin/env python3
"""
Development setup script for ProtoScribe
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return result
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None


def main():
    """Main setup function"""
    print("Setting up ProtoScribe development environment...")
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        sys.exit(1)
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    run_command("pip install -e .", "Installing ProtoScribe package")
    run_command("pip install -e \".[dev]\"", "Installing development dependencies")
    
    # Download spaCy model
    print("\n🔤 Setting up NLP models...")
    run_command("python -m spacy download en_core_web_sm", "Downloading spaCy English model")
    
    # Create necessary directories
    print("\n📁 Creating directories...")
    directories = ["uploads", "logs"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    # Copy environment file
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_example.exists() and not env_file.exists():
        print("\n⚙️ Setting up environment file...")
        env_file.write_text(env_example.read_text())
        print("✓ Created .env file from .env.example")
        print("📝 Please edit .env file to add your API keys")
    
    # Initialize database
    print("\n🗄️ Setting up database...")
    run_command("python -c \"from src.protoscribe.models.database import engine, Base; Base.metadata.create_all(bind=engine); print('Database initialized')\"", "Initializing database")
    
    # Install pre-commit hooks if available
    if Path(".pre-commit-config.yaml").exists():
        print("\n🔧 Setting up pre-commit hooks...")
        run_command("pre-commit install", "Installing pre-commit hooks")
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file to add your API keys")
    print("2. Run: uvicorn src.protoscribe.main:app --reload")
    print("3. Open http://localhost:8000/docs to view the API documentation")


if __name__ == "__main__":
    main()
