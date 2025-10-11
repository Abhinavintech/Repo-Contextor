"""Markdown renderer for repository context."""

from typing import Dict, Any
from ..utils import get_language_from_extension


def render_markdown(root: str, repo_info: Dict[str, Any], tree_text: str, 
                   files: Dict[str, str], total_files: int, total_lines: int, recent_files=None, file_sizes=None) -> str:
    """Render repository context as markdown."""
    
    lines = []
    
    # Header
    lines.append(f"# Repository Context: {root}")
    lines.append("")
    
    # Repository info
    if repo_info.get("is_repo"):
        lines.append("## Git Repository Information")
        lines.append(f"- **Branch**: {repo_info.get('branch', 'N/A')}")
        lines.append(f"- **Commit**: {repo_info.get('commit', 'N/A')}")
        lines.append(f"- **Author**: {repo_info.get('author', 'N/A')}")
        lines.append(f"- **Date**: {repo_info.get('date', 'N/A')}")
    else:
        lines.append("## Repository Information")
        lines.append(f"- **Note**: {repo_info.get('note', 'Not a git repository')}")
    lines.append("")
    
    # Summary
    lines.append("## Summary")
    lines.append(f"- **Total Files**: {total_files}")
    lines.append(f"- **Total Lines**: {total_lines}")
    lines.append("")
    
    # Directory structure
    lines.append("## Directory Structure")
    lines.append("```")
    lines.append(tree_text)
    lines.append("```")
    lines.append("")

    # will produce recent files 
    # Recent files (fixed)
    if recent_files:
        lines.append("## Recent Changes")
        for file, age in recent_files.items():
            lines.append(f"- {file} (modified {age})")
        lines.append("")
    
    # File contents
    lines.append("## File Contents")
    lines.append("")
    
    for file_path, content in sorted(files.items()):
        if file_sizes and file_path in file_sizes:
            size_bytes = file_sizes[file_path]
            lines.append(f"### {file_path} ({size_bytes} bytes)")
        else:
            lines.append(f"### {file_path}")
        lines.append("")
        
        # Detect language for syntax highlighting
        language = get_language_from_extension(file_path)
        
        lines.append(f"```{language}")
        lines.append(content)
        lines.append("```")
        lines.append("")
    
    return "\n".join(lines)
