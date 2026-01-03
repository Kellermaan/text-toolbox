#!/bin/bash
# Clean up unnecessary files and directories

echo "Cleaning up unnecessary files..."

# Remove virtual environment directories from root
if [ -d ".venv" ]; then
    echo "Removing .venv/"
    rm -rf .venv
fi

if [ -d ".venv-1" ]; then
    echo "Removing .venv-1/"
    rm -rf .venv-1
fi

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.pyo" -delete 2>/dev/null

# Remove temporary files
if [ -d "backend/temp" ]; then
    echo "Cleaning backend/temp/"
    rm -rf backend/temp/*
fi

echo "✅ Cleanup complete!"
