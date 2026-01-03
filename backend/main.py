"""
Text Toolbox - Comprehensive Text Processing Toolkit
Main application entry point
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil
from pathlib import Path
from typing import List

# Import tool modules
from tools.md_merger import MdMerger

app = FastAPI(
    title="Text Toolbox",
    description="Comprehensive Text Processing Toolkit",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary files directory
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

# Tool registry - makes it easy to extend with new features
TOOLS_REGISTRY = {
    "md_merger": {
        "name": "Markdown File Merger",
        "description": "Merge multiple date-named Markdown files in chronological order",
        "endpoint": "/tools/md-merger",
        "handler": MdMerger()
    }
}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Text Toolbox",
        "version": "1.0.0",
        "tools": [
            {
                "id": tool_id,
                "name": tool_info["name"],
                "description": tool_info["description"],
                "endpoint": tool_info["endpoint"]
            }
            for tool_id, tool_info in TOOLS_REGISTRY.items()
        ]
    }


@app.get("/api/tools")
async def get_tools():
    """Get all available tools list"""
    return {
        "tools": [
            {
                "id": tool_id,
                "name": tool_info["name"],
                "description": tool_info["description"],
                "endpoint": tool_info["endpoint"]
            }
            for tool_id, tool_info in TOOLS_REGISTRY.items()
        ]
    }


@app.post("/api/tools/md-merger")
async def merge_md_files(files: List[UploadFile] = File(...)):
    """
    Merge Markdown files
    Accepts multiple file uploads (can be multiple files from a folder or extracted files)
    """
    print(f"\n{'='*50}")
    print(f"Received {len(files)} files")
    for f in files:
        print(f"  - {f.filename}")
    print(f"{'='*50}")
    try:
        # Create temporary directory
        temp_dir = TEMP_DIR / "upload"
        temp_dir.mkdir(exist_ok=True)
        
        # Save uploaded files
        uploaded_files = []
        for file in files:
            file_path = temp_dir / file.filename
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            uploaded_files.append(file_path)
        
        # Call merge tool
        merger = TOOLS_REGISTRY["md_merger"]["handler"]
        result_file = await merger.merge(uploaded_files)
        
        # Clean up uploaded temporary files
        for file_path in uploaded_files:
            file_path.unlink(missing_ok=True)
        
        # Return merged file
        return FileResponse(
            result_file,
            media_type="text/markdown",
            filename=result_file.name,
            background=None
        )
        
    except ValueError as e:
        # User error (no valid files, wrong format, etc.)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Server error
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        print(f"Error in md-merger: {error_detail}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/tools/md-merger/zip")
async def merge_md_files_from_zip(file: UploadFile = File(...)):
    """
    Extract and merge Markdown files from ZIP archive
    """
    print(f"\n{'='*50}")
    print(f"Received ZIP file: {file.filename}")
    print(f"{'='*50}")
    try:
        import zipfile
        
        # Create temporary directories
        temp_dir = TEMP_DIR / "upload_zip"
        extract_dir = TEMP_DIR / "extracted"
        temp_dir.mkdir(exist_ok=True)
        extract_dir.mkdir(exist_ok=True)
        
        # Save ZIP file
        zip_path = temp_dir / file.filename
        with open(zip_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Extract ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Find all .md files recursively (excluding system folders like __MACOSX)
        md_files = []
        for f in extract_dir.rglob("*.md"):
            # Get relative path parts from extract_dir
            relative_parts = f.relative_to(extract_dir).parts
            # Filter out system/hidden folders
            if not any(part.startswith('.') or part.startswith('__MACOSX') for part in relative_parts):
                md_files.append(f)
        
        if not md_files:
            raise ValueError("No .md files found in the ZIP archive")
        
        print(f"Found {len(md_files)} .md files in ZIP: {[f.name for f in md_files]}")
        
        # Call merge tool
        merger = TOOLS_REGISTRY["md_merger"]["handler"]
        result_file = await merger.merge(md_files)
        
        # Clean up temporary files
        shutil.rmtree(temp_dir, ignore_errors=True)
        shutil.rmtree(extract_dir, ignore_errors=True)
        
        # Return merged file
        return FileResponse(
            result_file,
            media_type="text/markdown",
            filename=result_file.name,
            background=None
        )
        
    except ValueError as e:
        # User error (no valid files, wrong format, etc.)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Server error
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        print(f"Error in md-merger/zip: {error_detail}")
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up temporary files on application shutdown"""
    shutil.rmtree(TEMP_DIR, ignore_errors=True)


if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("Starting Text Toolbox Backend")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000)
