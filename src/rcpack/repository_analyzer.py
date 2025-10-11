"""Repository analysis class that encapsulates repository data and operations."""

import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta

from .gitinfo import get_git_info
from .discover import discover_files
from .io_utils import is_binary_file, read_text_safely


class RepositoryAnalyzer:
    """Encapsulates repository path and provides analysis methods.
    
    Similar to how JavaScript Data class combines numbers with sum() and average(),
    this class combines repository path with analysis operations like git info,
    file discovery, and file processing.
    """
    
    def __init__(self, repo_path: Path):
        """Initialize analyzer with repository path."""
        self.repo_path = repo_path.resolve()
        if not self.repo_path.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")
    
    def get_git_info(self) -> Dict[str, Any]:
        """Get git repository information."""
        return get_git_info(self.repo_path)
    
    def discover_files(self, include_patterns: List[str] = None, 
                      exclude_patterns: List[str] = None) -> List[Path]:
        """Discover files in the repository."""
        return discover_files(
            [self.repo_path], 
            self.repo_path, 
            include_patterns or [], 
            exclude_patterns or []
        )
    
    def get_recent_files(self, files: List[Path], days: int = 7) -> List[Path]:
        """Filter files to only those modified in the last N days."""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_files = []
        
        for file_path in files:
            try:
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if mtime >= cutoff_date:
                    recent_files.append(file_path)
            except Exception:
                # Skip files we can't read
                continue
                
        return recent_files
    
    def process_file(self, file_path: Path, verbose: bool = False) -> Tuple[str, str, str]:
        """Process a single file and return its data.
        
        Returns:
            tuple: (relative_path_str, content, file_size)
        """
        relative_path = file_path.relative_to(self.repo_path)
        relative_path_str = str(relative_path)
        
        if verbose:
            print(f"Reading file: {relative_path}", file=sys.stderr)
            
        file_size = file_path.stat().st_size
        
        # Check if file is binary first
        if is_binary_file(file_path):
            if verbose:
                print(f"Skipping binary file: {relative_path}", file=sys.stderr)
            content = f"[Binary file skipped: {file_path.name}, {file_size} bytes]"
            return relative_path_str, content, str(file_size)
        
        # Use robust text reading with encoding fallbacks
        try:
            content, encoding_used, truncated = read_text_safely(file_path)
            if truncated:
                if verbose:
                    print(f"File truncated: {relative_path}", file=sys.stderr)
                content += f"\n\n[... TRUNCATED to first 16KB ...]"
            return relative_path_str, content, str(file_size)
        except Exception:
            if verbose:
                print(f"Error reading file: {relative_path}", file=sys.stderr)
            raise  # Re-raise to handle in calling code