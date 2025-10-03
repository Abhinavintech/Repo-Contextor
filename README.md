# Repo-Contextor

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful Repository Context Packager CLI tool that analyzes local git repositories and creates comprehensive text files containing repository content optimized for sharing with Large Language Models (LLMs).

## Overview

When developers want to get help from ChatGPT, Claude, or other LLMs about their code, they often struggle with how to share their codebase effectively. Common problems include:

- **Lost Context**: Copy-pasting individual files loses important project structure and relationships
- **Missing Dependencies**: LLMs can't see how files connect or what libraries are used
- **Incomplete Picture**: Hard to convey the overall architecture and organization
- **Manual Work**: Time-consuming to gather and format relevant code

**Repo-Contextor** solves this by automatically collecting and formatting repository content into a single, well-structured text file that provides rich context to LLMs, enabling them to give much better assistance with your code.

## Features

- **Git Integration**: Extracts commit SHA, branch, author, and date information
- **Project Structure**: Generates a clear directory tree visualization
- **File Content Packaging**: Includes file contents with syntax highlighting
- **Smart File Discovery**: Recursively scans directories with intelligent filtering
- **Binary File Detection**: Automatically skips binary files
- **Error Handling**: Gracefully handles permission errors and provides helpful messages
- **Multiple Output Formats**: Supports Markdown, JSON, and YAML formats
- **Flexible Output**: Write to stdout or save to a file
- **Recent Changes Filter**: Give the files which are updated in last 7days with the time when it was recently modified.

## Installation

### Prerequisites

- Python 3.9 or higher
- Git (for git repository analysis)

### For End Users

```bash
# Clone and install
git clone https://github.com/yourusername/Repo-Contextor.git
cd Repo-Contextor
pip install -e .
```

### For Contributors & Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/Repo-Contextor.git
cd Repo-Contextor

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .
```

## Usage

### Basic Examples

```bash
# Package current directory to terminal
repo-contextor .

# Package a specific directory
repo-contextor /path/to/your/project

# Save output to a file
repo-contextor . -o my-project-context.md

# Generate JSON format
repo-contextor . -f json -o context.json

# Generate YAML format
repo-contextor . -f yaml -o context.yaml

# Include only files modified in the last 7 days
repo-contextor . --recent

# Combine with output file
repo-contextor . --recent -o recent-changes.md
```

### Command Line Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `path` | - | Repository path to analyze (default: current directory) | `repo-contextor /path/to/project` |
| `--output` | `-o` | Output file path (default: stdout) | `-o context.md` |
| `--format` | `-f` | Output format: text, json, yaml (default: text) | `-f json` |
| `--help` | `-h` | Show help message | `-h` |
| `--recent`  | `-r`  | Include only files modified in the last 7 days    | `repo-contextor . -r -o recent.md` |

### Advanced Examples

```bash
# Analyze different repository
repo-contextor /path/to/other/project -o other-project.md

# Generate JSON for API consumption
repo-contextor . -f json -o api-context.json

# Create YAML configuration
repo-contextor . -f yaml -o project-config.yaml

# Generate files which are changed recently in 7 days
repo-contextor . -r --output recent-changes.txt

```
## Configuration via TOML

Repo-Contextor supports configuration through a `.repo-contextor.toml` file in the current working directory.  
This file allows you to avoid typing the same CLI arguments every time.

Example `.repo-contextor.toml`:

```toml
# Output file to write results
output = "context.yaml"

# Output format: text, json, or yaml
format = "yaml"

# Limit to files modified in the last 7 days
recent = true

# Repository path to analyze (default = current directory)
path = "."
```
### Rules
- If the `.repo-contextor.toml` file is **missing**, the tool falls back to defaults.  
- If the file is **present but invalid TOML**, the tool prints a clear error message and exits with status code 1.  
- **Unknown keys** in the TOML file are ignored (safe for future extensions).  
- **Precedence** of settings is:
  1. Command-line arguments (highest priority)  
  2. Values from `.repo-contextor.toml`  
  3. Built-in defaults (lowest priority)
     
## Output Format

The tool generates a structured text file with the following sections:

### 1. Repository Context Header
Project path and identification

### 2. Git Repository Information
- Current branch
- Latest commit SHA
- Last commit author
- Last commit date

### 3. Summary Statistics
- Total number of files processed
- Total lines of code

### 4. Directory Structure
Clean tree visualization showing project organization

### 5. Recent Changes (if `--recent` is used)

- Lists files modified in the last 7 days.
- Shows relative file paths along with how long ago each file was modified
- Helps focus on recently updated parts of the project.
- Can be combined with `--output` or `--format` to save or change the output type.


### 5. File Contents
Each file's content with:
- Clear file path headers
- Appropriate syntax highlighting language tags
- Complete file contents

## Example Output

When you run `repo-contextor .`, the output looks like this:

````markdown
# Repository Context: /path/to/your/project

## Git Repository Information
- **Branch**: main
- **Commit**: a1b2c3d4e5f6789...
- **Author**: John Doe <john@example.com>
- **Date**: Fri Sep 12 14:30:15 2025

## Summary
- **Total Files**: 15
- **Total Lines**: 1,247

## Directory Structure
```
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   └── test_main.py
├── README.md
└── requirements.txt
```
## Recent Changes
- src/main.py (modified 2 days ago)
- src/utils/helpers.py (modified 5 days ago)

## File Contents

### src/main.py

```python
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
```

### README.md

```markdown
# My Project
This is a sample project.
```

## Summary
- Total files: 15
- Total lines: 1,247
````

## What Files Are Included

The tool includes most text files but automatically excludes:

### Excluded Directories
- `.git`, `.svn`, `.hg` (version control)
- `__pycache__`, `.pytest_cache` (Python cache)
- `node_modules`, `.venv`, `venv` (dependencies/environments)
- `.vscode`, `.idea` (IDE directories)
- `build`, `dist`, `target` (build directories)

### File Handling Rules
- **Text files**: All readable text files with common extensions
- **Binary files**: Automatically detected and skipped
- **Permission errors**: Skipped with graceful handling
- **Configuration files**: Includes pyproject.toml, package.json, etc.

### Included File Types
- Source code: `.py`, `.js`, `.ts`, `.java`, `.cpp`, `.c`, `.go`, `.rs`, etc.
- Web files: `.html`, `.css`, `.scss`, `.vue`, `.jsx`, etc.
- Documentation: `.md`, `.txt`, `.rst`
- Configuration: `.json`, `.yaml`, `.toml`, `.ini`, `.cfg`
- Scripts: `.sh`, `.bash`, `.zsh`

## Error Handling

The tool handles errors gracefully:

| Error Type | Behavior |
|------------|----------|
| **Permission errors** | Skipped with warning |
| **Binary files** | Automatically detected and skipped |
| **Invalid paths** | Clear error messages |
| **Non-git repositories** | Works fine, shows "Not a git repository" |
| **Unreadable files** | Marked as "[Binary or unreadable file]" |

## Development

### Project Structure

```text
Repo-Contextor/
├── src/rcpack/              # Main package
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # Command-line interface
│   ├── discover.py         # File discovery logic
│   ├── gitinfo.py          # Git repository analysis
│   ├── treeview.py         # Directory tree generation
│   ├── packager.py         # Main orchestration
│   ├── io_utils.py         # File I/O utilities
│   └── renderer/           # Output formatters
│       ├── markdown.py     # Markdown renderer
│       └── jsonyaml.py     # JSON/YAML renderers
├── pyproject.toml          # Project configuration
├── LICENSE                 # MIT License
└── README.md              # This documentation
```

### Running Tests

```bash
# Test on current repository
repo-contextor . -o test-output.md

# Test different formats
repo-contextor . -f json | head -20
repo-contextor . -f yaml | head -20

# Test specific directory
repo-contextor src/ -o src-only.md
```

### Contributing

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/yourusername/Repo-Contextor.git
   cd Repo-Contextor
   ```
3. **Install for development:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```
4. **Make your changes and test:**
   ```bash
   repo-contextor . -o test.md
   ```
5. **Submit a pull request**

### Development Workflow

```bash
# 1. Setup development environment
git clone https://github.com/yourusername/Repo-Contextor.git
cd Repo-Contextor
python -m venv .venv
source .venv/bin/activate
pip install -e .

# 2. Make changes to the code
# Edit files in src/rcpack/

# 3. Test your changes
repo-contextor . -o test-output.md

# 4. Test different formats
repo-contextor . -f json -o test.json
repo-contextor . -f yaml -o test.yaml

# 5. Commit and push changes
git add .
git commit -m "Add new feature"
git push origin feature-branch
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Why Repo-Contextor?

The name "Repo-Contextor" combines "Repository" + "Context" + "or", representing the tool's purpose of providing rich context about code repositories in a format that's perfect for LLM interactions.

### Use Cases

- **AI Assistance**: Get better help from ChatGPT, Claude, or GitHub Copilot
- **Code Reviews**: Share complete project context with team members
- **Documentation**: Create comprehensive project snapshots
- **Onboarding**: Help new team members understand project structure
- **Project Analysis**: Understand repository structure and dependencies

### Perfect for LLMs

The output format is specifically designed to work well with Large Language Models:
- Clear section headers for easy parsing
- Syntax highlighting markers for code blocks
- Structured metadata (git info, file locations)
- Complete project context in a single file
- Multiple output formats (Markdown, JSON, YAML)
- Optimized for token efficiency
