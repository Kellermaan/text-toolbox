# Startup script
cd "$(dirname "$0")"

echo "🚀 Starting Text Toolbox..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first"
    exit 1
fi

# Start services
docker-compose up -d

echo ""
echo "✅ Services started successfully!"
echo ""
echo "📝 Frontend: http://localhost:8080"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "View logs: docker-compose logs -f"
echo "Stop services: docker-compose down"
