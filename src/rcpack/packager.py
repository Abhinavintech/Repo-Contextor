from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable, Tuple

from rcpack.discover import discover_files
from rcpack.gitinfo import get_git_info, is_git_repo
from rcpack.io_utils import read_text_safely, is_binary_file
from rcpack.renderer import markdown as md_renderer
from rcpack.renderer.jsonyaml import render_json, render_yaml
from rcpack.treeview import render_tree
from rcpack.utils import get_language_from_extension


def _find_root(inputs: list[str]) -> Path:
    input_paths = [Path(input_path) for input_path in inputs]
    if len(input_paths) == 1 and Path(input_paths[0]).is_dir():
        return input_paths[0].resolve()
    parent_dirs = [path if path.is_dir() else path.parent for path in input_paths]
    common_root = Path(*Path.commonpath([str(path.resolve()) for path in parent_dirs]).split("/"))
    return common_root.resolve()


def build_package(
    inputs: list[str],
    include_patterns: list[str] | None,
    exclude_patterns: list[str] | None,
    max_file_bytes: int,
    fmt: str = "markdown",
) -> Tuple[str, dict]:
    root = _find_root(inputs)
    root_abs = root.resolve()

    repo_info = (
        get_git_info(root_abs) if is_git_repo(root_abs) else {
            "is_repo": False,
            "commit": None,
            "branch": None,
            "author": None,
            "date": None,
            "note": "Not a git repository",
        }
    )

    files = discover_files(
        inputs=[Path(input_path) for input_path in inputs],
        root=root_abs,
        include_patterns=include_patterns or [],
        exclude_patterns=exclude_patterns or [],
    )
    relative_files = [discovered_file.relative_to(root_abs) for discovered_file in files]

    project_tree = render_tree([relative_path.as_posix() for relative_path in relative_files])

    files_dict: dict[str, str] = {}
    file_sizes: dict[str, int] = {}
    total_lines = 0
    total_chars = 0

    for discovered_file in files:
        relative_path = discovered_file.relative_to(root_abs).as_posix()
        try:
            if is_binary_file(discovered_file):
                content = f"[binary file skipped: {discovered_file.name}, {discovered_file.stat().st_size} bytes]"
                files_dict[relative_path] = content
                file_sizes[relative_path] = discovered_file.stat().st_size
                total_chars += len(content)
                continue

            content, used_encoding, truncated = read_text_safely(discovered_file, max_bytes=max_file_bytes)
            total_lines += content.count("\n") + (1 if content and not content.endswith("\n") else 0)
            total_chars += len(content)

            if truncated:
                truncation_note = f"\n\n[... TRUNCATED to first {max_file_bytes} bytes ...]"
                content = content + truncation_note
                total_chars += len(truncation_note)

            files_dict[relative_path] = content
            file_sizes[relative_path] = discovered_file.stat().st_size
        except Exception as exc:
            print(f"[rcpack] error reading {relative_path}: {exc}", file=sys.stderr)
            continue

    # render in chosen format
    if fmt == "markdown":
        out_text = md_renderer.render_markdown(
            root=str(root_abs),
            repo_info=repo_info,
            tree_text=project_tree,
            files=files_dict,
            total_files=len(files_dict),
            total_lines=total_lines,
        )
    elif fmt == "json":
        out_text = render_json(
            root=str(root_abs),
            repo_info=repo_info,
            tree_text=project_tree,
            files=files_dict,
            total_files=len(files_dict),
            total_lines=total_lines,
            recent_files=None,
            file_sizes=file_sizes,
        )
    elif fmt == "yaml":
        out_text = render_yaml(
            root=str(root_abs),
            repo_info=repo_info,
            tree_text=project_tree,
            files=files_dict,
            total_files=len(files_dict),
            total_lines=total_lines,
            recent_files=None,
            file_sizes=file_sizes,
        )
    else:
        raise ValueError(f"Unsupported format: {fmt}")

    stats = {"files": len(files_dict), "lines": total_lines, "chars": total_chars}
    return out_text, stats
