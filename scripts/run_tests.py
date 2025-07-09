#!/usr/bin/env python3
"""
Run all tests and generate coverage report
"""

import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed with exit code {e.returncode}")
        return False


def main():
    """Main test runner"""
    print("Running ProtoScribe test suite...")
    
    # Ensure we're in the project root
    if not Path("pyproject.toml").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    success = True
    
    # Run linting
    print("\n🔍 Running code quality checks...")
    if not run_command("black --check src/ tests/", "Code formatting check (black)"):
        success = False
    
    if not run_command("flake8 src/ tests/", "Linting (flake8)"):
        success = False
    
    if not run_command("mypy src/", "Type checking (mypy)"):
        success = False
    
    # Run tests with coverage
    print("\n🧪 Running tests...")
    if not run_command("pytest tests/ -v --cov=src/protoscribe --cov-report=html --cov-report=term", "Running test suite"):
        success = False
    
    # Generate coverage report
    print("\n📊 Coverage report generated in htmlcov/index.html")
    
    if success:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
