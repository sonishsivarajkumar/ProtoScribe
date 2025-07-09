#!/usr/bin/env python3
"""
Quick start script for ProtoScribe
This script helps you get ProtoScribe up and running quickly
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path
import time


def print_header():
    """Print welcome header"""
    print("=" * 60)
    print("🩺 ProtoScribe - Clinical Trial Protocol AI Optimizer")
    print("=" * 60)
    print()


def check_requirements():
    """Check system requirements"""
    print("🔍 Checking system requirements...")
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ Please run this script from the ProtoScribe project root")
        return False
    
    print("✓ Project structure verified")
    return True


def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Install the package and dependencies
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], check=True, capture_output=True)
        print("✓ Core dependencies installed")
        
        # Try to install spaCy model
        try:
            subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True, capture_output=True)
            print("✓ spaCy English model downloaded")
        except subprocess.CalledProcessError:
            print("⚠️  spaCy model download failed (optional)")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def setup_environment():
    """Setup environment file"""
    print("\n⚙️  Setting up environment...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        env_file.write_text(env_example.read_text())
        print("✓ Created .env file from template")
        print("💡 Edit .env file to add your API keys for full functionality")
    elif env_file.exists():
        print("✓ Environment file already exists")
    else:
        # Create basic .env file
        basic_env = """# ProtoScribe Environment Configuration
DATABASE_URL=sqlite:///./protoscribe.db
SECRET_KEY=dev-secret-key-change-in-production
DEBUG=true

# Add your API keys here for AI features
# OPENAI_API_KEY=your_key_here
# ANTHROPIC_API_KEY=your_key_here
"""
        env_file.write_text(basic_env)
        print("✓ Created basic .env file")


def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ["uploads", "logs"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created {directory}/ directory")


def start_server():
    """Start the FastAPI server"""
    print("\n🚀 Starting ProtoScribe server...")
    print("   Server will start at: http://localhost:8000")
    print("   API docs available at: http://localhost:8000/docs")
    print("   Press Ctrl+C to stop the server")
    print()
    
    try:
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "src.protoscribe.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to start server: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -e .")
        print("2. Check if port 8000 is available")
        print("3. Verify your Python environment")


def run_demo():
    """Run a quick demo"""
    print("\n🎯 Running quick functionality test...")
    
    try:
        # Test imports
        from src.protoscribe.services.document_processor import DocumentProcessor
        from src.protoscribe.services.compliance_checker import ComplianceChecker
        
        print("✓ Core modules imported successfully")
        
        # Test document processor
        processor = DocumentProcessor()
        print("✓ Document processor initialized")
        
        # Test compliance checker
        checker = ComplianceChecker()
        print("✓ Compliance checker initialized")
        
        print("✓ All core components are working!")
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False


def main():
    """Main function"""
    print_header()
    
    if not check_requirements():
        sys.exit(1)
    
    print("\nWhat would you like to do?")
    print("1. 🚀 Quick start (install deps + start server)")
    print("2. 📦 Install dependencies only")
    print("3. 🎯 Run functionality test")
    print("4. 🌐 Start server only")
    print("5. 📖 Show project info")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        # Quick start
        if install_dependencies():
            setup_environment()
            create_directories()
            if run_demo():
                print("\n🎉 Setup complete! Starting server...")
                time.sleep(2)
                start_server()
    
    elif choice == "2":
        # Install dependencies
        install_dependencies()
        setup_environment()
        create_directories()
        print("\n✅ Dependencies installed successfully!")
    
    elif choice == "3":
        # Run demo
        run_demo()
    
    elif choice == "4":
        # Start server only
        start_server()
    
    elif choice == "5":
        # Show project info
        print("\n📖 ProtoScribe Project Information")
        print("-" * 40)
        print("• Clinical Trial Protocol AI Optimizer")
        print("• Validates protocols against CONSORT/SPIRIT guidelines")
        print("• Provides AI-powered suggestions for improvement")
        print("• FastAPI backend with React frontend")
        print("• Supports PDF, DOCX, and TXT file uploads")
        print("\nProject structure:")
        print("• src/protoscribe/     - Main application code")
        print("• guidelines/          - CONSORT/SPIRIT knowledge base")
        print("• tests/              - Test suite")
        print("• frontend/           - React frontend (optional)")
        print("• scripts/            - Development utilities")
        print("\nNext steps:")
        print("1. Run this script with option 1 for quick start")
        print("2. Edit .env file to add your API keys")
        print("3. Access http://localhost:8000/docs for API documentation")
    
    else:
        print("❌ Invalid choice")
        sys.exit(1)


if __name__ == "__main__":
    main()
