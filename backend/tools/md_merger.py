"""
Markdown File Merger Tool
Merges multiple date-named Markdown files in chronological order
"""
import re
from pathlib import Path
from typing import List
from datetime import datetime
from .base import BaseTool


class MdMerger(BaseTool):
    """Markdown file merger tool"""
    
    @property
    def name(self) -> str:
        return "Markdown File Merger"
    
    @property
    def description(self) -> str:
        return "Merge multiple date-named Markdown files in chronological order"
    
    def _extract_date_from_filename(self, filename: str) -> datetime | None:
        """
        Extract date from filename
        Supports formats: 20250410.md, 2025-04-10.md, 20250410_something.md, etc.
        """
        # Try matching YYYYMMDD format
        match = re.search(r'(\d{4})(\d{2})(\d{2})', filename)
        if match:
            year, month, day = match.groups()
            try:
                return datetime(int(year), int(month), int(day))
            except ValueError:
                return None
        
        # Try matching YYYY-MM-DD format
        match = re.search(r'(\d{4})-(\d{2})-(\d{2})', filename)
        if match:
            year, month, day = match.groups()
            try:
                return datetime(int(year), int(month), int(day))
            except ValueError:
                return None
        
        return None
    
    def _format_date(self, date: datetime) -> str:
        """Format date as YYYY-MM-DD"""
        return date.strftime("%Y-%m-%d")
    
    def _read_file_content(self, file_path: Path) -> str:
        """Read file content and remove the first H1 heading if it exists"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
        except UnicodeDecodeError:
            # Try other encodings
            with open(file_path, 'r', encoding='gbk') as f:
                content = f.read().strip()
        
        # Remove first H1 heading (# Title) if present
        lines = content.split('\n')
        if lines and lines[0].startswith('# '):
            # Remove the H1 line and any immediately following empty lines
            lines = lines[1:]
            while lines and lines[0].strip() == '':
                lines = lines[1:]
            content = '\n'.join(lines)
        
        return content.strip()
    
    async def merge(self, file_paths: List[Path]) -> Path:
        """
        Main method to merge files
        
        Args:
            file_paths: List of file paths
            
        Returns:
            Path to the merged file
        """
        print(f"Received {len(file_paths)} files to merge")
        
        # Filter and parse files
        file_data = []
        for file_path in file_paths:
            print(f"Processing file: {file_path.name}")
            if file_path.suffix.lower() == '.md':
                date = self._extract_date_from_filename(file_path.name)
                if date:
                    print(f"  -> Date extracted: {date}")
                    content = self._read_file_content(file_path)
                    print(f"  -> Content length: {len(content)} chars")
                    file_data.append({
                        'date': date,
                        'content': content,
                        'filename': file_path.name
                    })
                else:
                    print(f"  -> No date found in filename: {file_path.name}")
        
        if not file_data:
            raise ValueError("No Markdown files with date format found")
        
        # Sort by date
        file_data.sort(key=lambda x: x['date'])
        
        # Get year (use the year from the first file)
        year = file_data[0]['date'].year
        
        # Build merged content
        merged_content = f"# {year}\n\n"
        
        for item in file_data:
            date_str = self._format_date(item['date'])
            content = item['content']
            
            # Add H2 heading and content
            merged_content += f"## {date_str}\n\n"
            merged_content += f"{content}\n\n"
            merged_content += "---\n\n"
        
        # Remove trailing separator and empty lines
        merged_content = merged_content.rstrip('\n').rstrip('-').rstrip('\n') + '\n'
        
        # Save merged file
        output_dir = Path("temp/output")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{year}.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(merged_content)
        
        return output_file
    
    async def process(self, *args, **kwargs) -> Path:
        """Implement the base class process method"""
        file_paths = kwargs.get('file_paths', [])
        return await self.merge(file_paths)
