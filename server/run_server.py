#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from populate_data import create_sample_data
    print("Running populate_data...")
    create_sample_data()
    
    # Test the API
    from app.main import app
    print("Starting server...")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you have installed the requirements:")
    print("pip install -r requirements.txt")
except Exception as e:
    print(f"Error: {e}")