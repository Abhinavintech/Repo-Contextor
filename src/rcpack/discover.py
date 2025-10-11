"""File discovery module for repository analysis."""

from pathlib import Path
from typing import List
import fnmatch
from .utils import DEFAULT_INCLUDE_EXTENSIONS, ALWAYS_INCLUDE_FILE_NAMES, SKIP_DIRECTORY_NAMES


def discover_files(
    inputs: List[Path],
    root: Path,
    include_patterns: List[str],
    exclude_patterns: List[str],
) -> List[Path]:
    """Discover relevant files.

    - inputs: list of files/dirs to scan
    - root: common project root; patterns are matched against POSIX paths relative to root
    - include_patterns: glob patterns to include (if empty, use sensible defaults)
    - exclude_patterns: glob patterns to exclude
    Returns a list of absolute Paths to files.
    """

    def matches_any(patterns: List[str], rel_posix: str) -> bool:
        return any(fnmatch.fnmatch(rel_posix, pat) for pat in patterns)

    def should_take(file_path: Path) -> bool:
        rel_posix = file_path.relative_to(root).as_posix()
        if exclude_patterns and matches_any(exclude_patterns, rel_posix):
            return False
        if include_patterns:
            return matches_any(include_patterns, rel_posix)
        # default include logic
        return file_path.name in ALWAYS_INCLUDE_FILE_NAMES or file_path.suffix.lower() in DEFAULT_INCLUDE_EXTENSIONS

    discovered: list[Path] = []
    seen = set()

    for input_item in inputs:
        resolved_path = input_item.resolve()
        if resolved_path.is_file():
            # Skip if excluded or in skipped directory
            if any(part in SKIP_DIRECTORY_NAMES for part in resolved_path.parts):
                continue
            if should_take(resolved_path):
                path_key = resolved_path.as_posix()
                if path_key not in seen:
                    seen.add(path_key)
                    discovered.append(resolved_path)
        elif resolved_path.is_dir():
            for child in resolved_path.rglob('*'):
                if not child.is_file():
                    continue
                if any(part in SKIP_DIRECTORY_NAMES for part in child.parts):
                    continue
                if should_take(child):
                    child_key = child.resolve().as_posix()
                    if child_key not in seen:
                        seen.add(child_key)
                        discovered.append(child.resolve())

    return sorted(discovered)