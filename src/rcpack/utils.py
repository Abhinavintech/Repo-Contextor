"""Utility functions shared across the rcpack package."""

from typing import Dict, Any, Optional, Set


# Shared constants for file discovery and processing
DEFAULT_INCLUDE_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h',
    '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala',
    '.html', '.css', '.scss', '.sass', '.less', '.vue', '.svelte',
    '.md', '.txt', '.rst', '.yaml', '.yml', '.json', '.toml', '.ini',
    '.cfg', '.conf', '.xml', '.sql', '.sh', '.bash', '.zsh', '.fish',
}

ALWAYS_INCLUDE_FILE_NAMES = {
    'README', 'LICENSE', 'CHANGELOG', 'CONTRIBUTING', 'Makefile',
    'requirements.txt', 'package.json', 'Cargo.toml', 'pyproject.toml',
    'setup.py', 'setup.cfg', 'pom.xml', 'build.gradle', '.gitignore', '.gitattributes'
}

SKIP_DIRECTORY_NAMES = {
    '.git', '.svn', '.hg', '__pycache__', '.pytest_cache',
    'node_modules', '.venv', 'venv', 'env', '.env',
    'build', 'dist', 'target', 'out', '.next', '.nuxt',
    '.idea', '.vscode', '.vs', 'coverage', '.coverage'
}


def get_language_from_extension(file_path_or_ext: str) -> str:
    """Get the language identifier for syntax highlighting from a file path or extension.
    
    Args:
        file_path_or_ext: Either a file path (e.g., 'src/main.py') or extension (e.g., '.py' or 'py')
    
    Returns:
        Language identifier for syntax highlighting (e.g., 'python', 'javascript')
    """
    # Extract extension from file path if needed
    if '.' in file_path_or_ext and not file_path_or_ext.startswith('.'):
        # It's a file path, extract the extension
        ext = file_path_or_ext.split('.')[-1].lower()
    else:
        # It's already an extension, clean it up
        ext = file_path_or_ext.lower().lstrip(".")
    
    # Comprehensive language mapping combining both existing mappings
    language_map = {
        'py': 'python', 'js': 'javascript', 'ts': 'typescript',
        'jsx': 'javascript', 'tsx': 'typescript',
        'java': 'java', 'cpp': 'cpp', 'c': 'c', 'h': 'c',
        'cs': 'csharp', 'php': 'php', 'rb': 'ruby',
        'go': 'go', 'rs': 'rust', 'swift': 'swift', 'kt': 'kotlin',
        'html': 'html', 'css': 'css', 'scss': 'scss', 'sass': 'sass',
        'json': 'json', 'yaml': 'yaml', 'yml': 'yaml',
        'toml': 'toml', 'xml': 'xml', 'sql': 'sql', 'sh': 'bash',
        'bash': 'bash', 'zsh': 'bash', 'fish': 'fish',
        'md': 'markdown', 'txt': 'text',
        'dockerfile': 'dockerfile', 'makefile': 'makefile'
    }
    
    return language_map.get(ext, '')


def build_repository_data(
    root: str,
    repo_info: Dict[str, Any],
    tree_text: str,
    files: Dict[str, str],
    total_files: int,
    total_lines: int,
    recent_files: Optional[Dict[str, str]] = None,
    file_sizes: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Build the standard repository data structure used by all renderers.
    
    Args:
        root: Repository root path
        repo_info: Git repository information
        tree_text: Directory tree text representation
        files: Dictionary of file paths to content
        total_files: Total number of files
        total_lines: Total number of lines
        recent_files: Optional dict of recently modified files
        file_sizes: Optional dict of file sizes
        
    Returns:
        Standardized data dictionary for rendering
    """
    return {
        "root": root,
        "repo_info": repo_info,
        "structure": tree_text,
        "recent_changes": recent_files or {},
        "files": files,
        "file_sizes": file_sizes or {},
        "summary": {"total_files": total_files, "total_lines": total_lines},
    }


def calculate_total_lines(content_dict: Dict[str, str]) -> int:
    """Calculate the total number of lines from a dictionary of file contents.
    
    Args:
        content_dict: Dictionary mapping file paths to their content
        
    Returns:
        Total number of lines across all files
    """
    return sum(len(content.splitlines()) for content in content_dict.values())


def calculate_total_characters(content_dict: Dict[str, str]) -> int:
    """Calculate the total number of characters from a dictionary of file contents.
    
    Args:
        content_dict: Dictionary mapping file paths to their content
        
    Returns:
        Total number of characters across all files
    """
    return sum(len(content) for content in content_dict.values())