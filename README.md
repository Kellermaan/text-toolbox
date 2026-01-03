# 📝 Text Toolbox

An extensible and beautifully designed web-based text processing toolbox with multiple text processing capabilities.

[中文文档](README.zh.md)

## ✨ Features

- 🎨 **Beautiful Web Interface** - Modern gradient design with drag-and-drop file upload
- 🔧 **Easy to Extend** - Plugin architecture for easy addition of new features
- 🚀 **High Performance** - Asynchronous backend based on FastAPI
- 📦 **Flexible Input** - Supports multiple file selection and ZIP archives
- 🌐 **Cross-Platform** - Web-based, works in any browser

## 🛠️ Current Features

### 1. Markdown File Merger

Merges multiple date-named Markdown files in chronological order into a single file.

**Supported filename formats:**
- `20250410.md`
- `2025-04-10.md`
- `20250410_notes.md`

**Merge rules:**
- Output filename is the year (e.g., `2025.md`)
- H1 heading is the year (e.g., `# 2025`)
- H2 headings are formatted dates (e.g., `## 2025-03-09`)
- Each file's content follows its corresponding date heading
- Files are separated by horizontal rules `---`
- Sorted in ascending date order

**Usage:**
1. Upload multiple .md files, or
2. Upload a .zip archive containing .md files

## 🏗️ Project Structure

```
text-toolbox/
├── backend/                 # Backend code
│   ├── main.py             # FastAPI application entry point
│   ├── requirements.txt    # Python dependencies
│   ├── tools/              # Tool modules directory
│   │   ├── __init__.py
│   │   ├── base.py         # Base tool class
│   │   └── md_merger.py    # Markdown merger tool
│   └── temp/               # Temporary files directory
├── frontend/               # Frontend code
│   └── index.html         # Single page application
├── docker-compose.yml     # Docker Compose file
├── Dockerfile            # Docker image
└── README.md             # Project documentation
```

## 🚀 Quick Start

### Option 1: Using Docker (Recommended)

```bash
# Start all services
./start.sh        # Linux/Mac
start.bat         # Windows

# Or manually:
docker-compose up -d
```

Access: http://localhost:8080

### Option 2: Local Development

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Start backend
python main.py
```

Backend API: http://localhost:8000

In another terminal:
```bash
# Start frontend
cd frontend
python -m http.server 8080
```

Frontend: http://localhost:8080

## 📚 API Documentation

After starting the backend, visit http://localhost:8000/docs to view the auto-generated API documentation.

### Main Endpoints

- `GET /` - Get API information and tool list
- `GET /api/tools` - Get all available tools
- `POST /api/tools/md-merger` - Merge multiple MD files
- `POST /api/tools/md-merger/zip` - Extract and merge MD files from ZIP

## 🔧 Adding New Features

This project uses a plugin architecture, making it very simple to add new features:

### 1. Create Tool Class

Create a new tool file in `backend/tools/` directory, inheriting from `BaseTool`:

```python
# backend/tools/your_tool.py
from .base import BaseTool

class YourTool(BaseTool):
    @property
    def name(self) -> str:
        return "Your Tool Name"
    
    @property
    def description(self) -> str:
        return "Tool description"
    
    async def process(self, *args, **kwargs):
        # Implement your processing logic
        pass
```

### 2. Register Tool

Register your tool in `backend/main.py`:

```python
from tools.your_tool import YourTool

TOOLS_REGISTRY = {
    "md_merger": {...},
    "your_tool": {
        "name": "Your Tool Name",
        "description": "Tool description",
        "endpoint": "/tools/your-tool",
        "handler": YourTool()
    }
}
```

### 3. Add API Endpoint

Add the corresponding API endpoint in `backend/main.py`:

```python
@app.post("/api/tools/your-tool")
async def your_tool_endpoint(file: UploadFile = File(...)):
    # Processing logic
    pass
```

### 4. Update Frontend Interface

Add a new tool card and interaction logic in `frontend/index.html`.

## 🐳 Docker Deployment

The project includes complete Docker configuration for one-click deployment:

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔍 Example

### Input Files

```
folder/
├── 20250101.md
├── 20250102.md
└── 20250103.md
```

**20250101.md:**
```markdown
First day of 2025, Happy New Year!
```

**20250102.md:**
```markdown
Starting to plan for the new year.
```

### Output File (2025.md)

```markdown
# 2025

## 2025-01-01

First day of 2025, Happy New Year!

---

## 2025-01-02

Starting to plan for the new year.

---
```

## 🛣️ Roadmap

- [x] Markdown file merger feature
- [ ] Text format conversion (MD/TXT/PDF, etc.)
- [ ] Batch file renaming
- [ ] Text statistics and analysis
- [ ] Regex batch replacement
- [ ] CSV/Excel data processing
- [ ] Text deduplication tool

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

MIT License

## 👨‍💻 Tech Stack

- **Backend**: FastAPI (Python 3.8+)
- **Frontend**: Native HTML/CSS/JavaScript
- **Deployment**: Docker + Docker Compose