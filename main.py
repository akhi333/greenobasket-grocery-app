#!/usr/bin/env python3
"""
GreenObasket - Premium Grocery App
Main entry point for deployment
"""

import os
import sys

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Import the Flask app
from app import app

if __name__ == '__main__':
    # Get port from environment variable (for deployment) or default to 5001
    port = int(os.environ.get('PORT', 5001))
    
    # Run the app
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=port,
        debug=False      # Disable debug in production
    ) 