#!/usr/bin/env python3
"""
Run script for AI-Based Personal Fitness Assistant
Simplifies running the application
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    from app.app import app, db, load_model

    # Initialize database
    with app.app_context():
        db.create_all()
        print("Database initialized!")

        # Load ML model
        if load_model():
            print("ML model loaded successfully!")
        else:
            print("WARNING: ML model not found. Using fallback calculations.")

    # Start app
    print("\n" + "="*50)
    print("Starting Fitness Assistant...")
    print("="*50)
    print("\nOpen your browser to: http://localhost:5000")
    print("Press Ctrl+C to stop\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
