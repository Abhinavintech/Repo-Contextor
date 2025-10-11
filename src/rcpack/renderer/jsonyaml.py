from __future__ import annotations
import json
from ..utils import build_repository_data

try:
    import yaml
except ImportError:
    yaml = None


def render_json(root, repo_info, tree_text, files, total_files, total_lines,recent_files=None, file_sizes=None) -> str:
    data = build_repository_data(
        root=root,
        repo_info=repo_info,
        tree_text=tree_text,
        files=files,
        total_files=total_files,
        total_lines=total_lines,
        recent_files=recent_files,
        file_sizes=file_sizes
    )
    return json.dumps(data, indent=2, ensure_ascii=False)


def render_yaml(root, repo_info, tree_text, files, total_files, total_lines,recent_files=None, file_sizes=None) -> str:
    if yaml is None:
        raise RuntimeError("PyYAML not installed; run `pip install pyyaml`")
    data = build_repository_data(
        root=root,
        repo_info=repo_info,
        tree_text=tree_text,
        files=files,
        total_files=total_files,
        total_lines=total_lines,
        recent_files=recent_files,
        file_sizes=file_sizes
    )
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
