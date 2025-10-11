#!/usr/bin/env python3
"""CLI for Repository Context Packager."""

from .config_loader import load_config

import argparse
import sys
from pathlib import Path
from .gitinfo import get_git_info
from .discover import discover_files
from .treeview import create_tree_view
from .renderer.markdown import render_markdown
from .renderer.jsonyaml import render_json, render_yaml
from .io_utils import write_output, is_binary_file, read_text_safely
from .repository_analyzer import RepositoryAnalyzer
from datetime import datetime, timedelta


def log_verbose(message: str, verbose: bool) -> None:
    """Log a message to stderr if verbose mode is enabled."""
    if verbose:
        print(message, file=sys.stderr)


def get_rendered_content(format_type: str, repo_path: str, repo_info: dict, tree_text: str, 
                        files_data: dict, total_files: int, total_lines: int, 
                        recent_files_info: dict, file_sizes: dict) -> str:
    """Get rendered content based on the specified format."""
    if format_type == "json":
        return render_json(
            repo_path, repo_info, tree_text, 
            files_data, total_files, total_lines,
            recent_files=recent_files_info,
            file_sizes=file_sizes
        )
    elif format_type == "yaml":
        return render_yaml(
            repo_path, repo_info, tree_text, 
            files_data, total_files, total_lines,
            recent_files=recent_files_info,
            file_sizes=file_sizes
        )
    else:  # text/markdown
        return render_markdown(
            repo_path, repo_info, tree_text, 
            files_data, total_files, total_lines,
            recent_files=recent_files_info,
            file_sizes=file_sizes
        )



def handle_output(content: str, output_path: str = None) -> None:
    """Handle output to either file or stdout."""
    if output_path:
        # Write to file
        write_output(output_path, content)
        print(f"Context package created: {output_path}")
    else:
        # Output to stdout
        print(content)


def main():
    parser = argparse.ArgumentParser(
        description="Package repository content for LLM context"
    )
    parser.add_argument(
        "path", 
        nargs="?", 
        default=".", 
        help="Repository path (default: current directory)"
    )
    parser.add_argument(
        "-o", "--output", 
        help="Output file path (default: stdout)"
    )
    parser.add_argument(
        "-f", "--format", 
        choices=["text", "json", "yaml"], 
        default="text",
        help="Output format (default: text)"
    )

    """ This will read -r from the console and able to search it with this"""
    parser.add_argument(
    "-r", "--recent",
    action="store_true",
    help="Include only files modified in the last 7 days"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print detailed progress information to stderr"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize repository analyzer
        log_verbose(f"Analyzing repository: {args.path}", args.verbose)
        analyzer = RepositoryAnalyzer(Path(args.path))
        
        # Get repository information using analyzer
        repo_info = analyzer.get_git_info()
        
        # Discover files using analyzer
        log_verbose(f"Discovering files in: {analyzer.repo_path}", args.verbose)
        discovered_files = analyzer.discover_files()
        log_verbose(f"Found {len(discovered_files)} files", args.verbose)
        
        # Filter to recent files if requested
        recent_files_info = {}
        if args.recent:
            recent_files = analyzer.get_recent_files(discovered_files, days=7)
            for recent_file in recent_files:
                try:
                    mtime = datetime.fromtimestamp(recent_file.stat().st_mtime)
                    recent_files_info[str(recent_file.relative_to(analyzer.repo_path))] = human_readable_age(mtime)     
                except Exception:
                    continue
            discovered_files = recent_files
        
        # Read file contents
        files_data = {}
        file_sizes = {}
        for file_path in discovered_files:
            try:
                relative_path_str, content, file_size = analyzer.process_file(file_path, args.verbose)
                files_data[relative_path_str] = content
                file_sizes[relative_path_str] = file_size
            except Exception:
                continue
        
        # Create tree view
        log_verbose("Generating directory tree", args.verbose)
        tree_text = create_tree_view(analyzer.repo_path, files_data)
        
        # Count totals
        total_files = len(files_data)
        total_lines = sum(len(content.splitlines()) for _, content in files_data.items())
        
        # Render based on format
        log_verbose(f"Rendering output in {args.format} format", args.verbose)
        content = get_rendered_content(
            args.format, str(analyzer.repo_path), repo_info, tree_text,
            files_data, total_files, total_lines,
            recent_files_info if args.recent else {},
            file_sizes
        )
        
        handle_output(content, args.output)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

# this will convert age and give us the difference
def human_readable_age(mtime: datetime) -> str:
    delta = datetime.now() - mtime
    days = delta.days
    seconds = delta.seconds
    if days > 0:
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif seconds >= 3600:
        hours = seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds >= 60:
        minutes = seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    else:
        return "just now"

if __name__ == "__main__":
    main()
