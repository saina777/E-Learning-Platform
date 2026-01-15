#!/bin/bash
# Build script for backend deployment

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Creating database tables..."
python3 -c "from app.db.session import engine; from app.db.base import Base; from app import models; Base.metadata.create_all(bind=engine)"

echo "Populating database with sample data..."
python3 populate_data.py

echo "Build complete!"
