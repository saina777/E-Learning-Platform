#!/usr/bin/env python3
import sys
import os

# Add the server directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.main import app
    import uvicorn
    
    print("🚀 Starting LearnFlow API server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API docs available at: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
except Exception as e:
    print(f"❌ Error starting server: {e}")
    print("💡 Make sure you have installed dependencies: pip install -r requirements.txt")