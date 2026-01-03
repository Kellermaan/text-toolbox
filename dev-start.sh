#!/bin/bash
# Complete startup script for local development

echo "🚀 Starting Text Toolbox in Local Development Mode"
echo ""

# Check if backend dependencies are installed
cd backend
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing backend dependencies..."
    pip install --break-system-packages -r requirements.txt
    echo ""
fi

# Start backend in background
echo "🔧 Starting backend server..."
python3 main.py &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""

# Wait for backend to start
sleep 3

# Start frontend
cd ../frontend
echo "🌐 Starting frontend server..."
echo "   Frontend: http://localhost:8080"
echo ""
echo "✅ All services started!"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Start frontend (this will keep the script running)
python3 -m http.server 8080

# Cleanup on exit
kill $BACKEND_PID 2>/dev/null
