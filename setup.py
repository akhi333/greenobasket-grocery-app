#!/usr/bin/env python3
"""
🌱 GreenObasket Setup Script
==========================

This script helps you set up and run the GreenObasket grocery delivery app.

Usage:
    python setup.py install    # Install dependencies
    python setup.py run        # Run the application
    python setup.py help       # Show this help
"""

import sys
import subprocess
import os
from pathlib import Path

def install_dependencies():
    """Install required Python packages."""
    print("🔧 Installing dependencies...")
    
    try:
        # Change to backend directory
        backend_dir = Path(__file__).parent / "backend"
        os.chdir(backend_dir)
        
        # Install requirements
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True, text=True)
        
        print("✅ Dependencies installed successfully!")
        print("\n📦 Installed packages:")
        print("  - Flask (web framework)")
        print("  - Flask-CORS (cross-origin requests)")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print(f"Output: {e.output}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

def run_application():
    """Run the GreenObasket application."""
    print("🚀 Starting GreenObasket application...")
    
    try:
        # Change to backend directory
        backend_dir = Path(__file__).parent / "backend"
        os.chdir(backend_dir)
        
        print("\n🌐 Application will be available at:")
        print("   Customer App: http://localhost:5001")
        print("   Admin Panel:  http://localhost:5001/admin")
        print("\n🔐 Admin credentials:")
        print("   Username: admin")
        print("   Password: greenbasket123")
        print("\n📱 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Run the Flask app
        subprocess.run([sys.executable, "app.py"], check=True)
        
    except KeyboardInterrupt:
        print("\n\n👋 GreenObasket stopped. Thanks for using our app!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

def show_help():
    """Display help information."""
    print(__doc__)
    print("\n🎯 Quick Start:")
    print("1. python setup.py install    # First time setup")
    print("2. python setup.py run        # Start the app")
    print("\n📁 Project Structure:")
    print("├── backend/        # Flask API server")
    print("├── frontend/       # HTML/CSS/JS files")
    print("├── docs/          # Documentation")
    print("└── static/        # Static assets")

def main():
    """Main setup script entry point."""
    if len(sys.argv) != 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "install":
        install_dependencies()
    elif command == "run":
        run_application()
    elif command == "help":
        show_help()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    main() 