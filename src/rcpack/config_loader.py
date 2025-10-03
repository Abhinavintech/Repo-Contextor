# src/rcpack/config_loader.py
"""
TOML config loader for Repo-Contextor.

Rules:
- Look for .repo-contextor.toml in the CURRENT directory
- If missing: ignore
- If present but invalid: print a clear error and exit(1)
- Only recognized keys are applied; unknown keys ignored
- Precedence: CLI > TOML > DEFAULTS
"""
from __future__ import annotations
import os, sys
from typing import Dict, Iterable, Any

try:
    import tomllib
    _loads = tomllib.loads
except ModuleNotFoundError:
    try:
        import tomli
        _loads = tomli.loads
    except ModuleNotFoundError:
        _loads = None

def _need_toml():
    if _loads is None:
        print("Error: TOML parser not available. Use Python 3.11+ or `pip install tomli`.", file=sys.stderr)
        sys.exit(1)

def _load_toml(dotfile: str) -> Dict[str, Any]:
    _need_toml()
    if not os.path.exists(dotfile):
        return {}
    try:
        with open(dotfile, "rb") as f:
            raw = f.read().decode("utf-8", errors="strict")
        data = _loads(raw)
        return data if isinstance(data, dict) else {}
    except Exception as e:
        print(f"Error: failed to parse {dotfile} as TOML.\n{e}", file=sys.stderr)
        sys.exit(1)

def _filter_known(d: Dict[str, Any], known: Iterable[str]) -> Dict[str, Any]:
    ks = set(known)
    return {k: v for k, v in d.items() if k in ks}

def _merge(defaults: Dict[str, Any], filecfg: Dict[str, Any], clicfg: Dict[str, Any], known: Iterable[str]) -> Dict[str, Any]:
    ks = set(known)
    out: Dict[str, Any] = {k: defaults.get(k) for k in ks}
    for src in (filecfg, clicfg):
        for k, v in src.items():
            if k in ks and v is not None:
                out[k] = v
    return out

def load_config(*, dotfile: str = ".repo-contextor.toml", defaults: Dict[str, Any] | None = None, cli_cfg: Dict[str, Any] | None = None, known_keys: Iterable[str] = ()) -> Dict[str, Any]:
    defaults = defaults or {}
    cli_cfg = cli_cfg or {}
    known = tuple(known_keys)
    filecfg = _filter_known(_load_toml(dotfile), known)
    return _merge(defaults, filecfg, cli_cfg, known)
