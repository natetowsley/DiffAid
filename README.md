# DiffAid
[![PyPI version](https://img.shields.io/pypi/v/diffaid)](https://pypi.org/project/diffaid/)
[![Python versions](https://img.shields.io/pypi/pyversions/diffaid)](https://pypi.org/project/diffaid/)
[![License](https://img.shields.io/pypi/l/diffaid)](https://github.com/natetowsley/diffaid/blob/master/LICENSE)
[![PyPI downloads](https://img.shields.io/pypi/dm/diffaid)](https://pypi.org/project/diffaid/)

AI-assisted git diff review CLI that catches bugs before you commit.

## Features

- **Smart Analysis** – Uses Gemini AI to review code changes  
- **CI Integration** – Exit codes for automated workflows  
- **Fast** – Reviews in seconds with Gemini Flash  
- **Clean Output** – Color-coded findings in your terminal  


## Installation

Install DiffAid using pip:

```bash
pip install diffaid
```

## Requirements

- Python 3.10+
- Git
- Gemini API key (free tier available)

## Setup
1. Get a free Gemini API key at: https://aistudio.google.com/apikey

2. Set the GEMINI_API_KEY environment variable.

### Option 1: Using .env file (Recommended)

Create a `.env` file in your project root:
```
GEMINI_API_KEY=your-key-here
```

### Option 2: Environment Variable

#### Mac / Linux:
```
export GEMINI_API_KEY="your-key-here"
```

#### Windows (PowerShell):
```
$env:GEMINI_API_KEY="your-key-here"
```
#### Permanent Setup

##### Mac / Linux
Add to ~/.bashrc or ~/.zshrc:
```
echo 'export GEMINI_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

##### Windows
Add as a system environment variable through System Properties, or use PowerShell:
```
[System.Environment]::SetEnvironmentVariable(
  'GEMINI_API_KEY',
  'your-key-here',
  'User'
)
```
## Usage

Stage your changes and run DiffAid:
```
git add .
diffaid
```

DiffAid will analyze your staged changes and report:

**Errors** – Critical issues that should be fixed

**Warnings** – Potential problems worth reviewing

**Notes** – Suggestions for improvement

## Command Options

- `diffaid` - Quick overview (default mode)
- `diffaid --detailed` or `diffaid -d` - Detailed line-by-line review with all suggestions
- `diffaid --json` - Output raw JSON instead of formatted text
- `diffaid --strict` - Treat warnings as errors (exit code 1)
- `diffaid --version` or `diffaid -v` - Show version and exit

## Example Output
```
Summary: Added user authentication with JWT tokens

ERROR: Hardcoded secret key detected
  → auth.py

WARNING: Missing error handling for database connection
  → db.py

NOTE: Consider adding rate limiting to login endpoint
  → routes.py

---
Found: 1 error, 1 warning, 1 note
```
## Exit Codes

DiffAid uses standard exit codes for CI/CD integration:

- 0 – No errors found (warnings are OK in normal mode)
- 1 – Errors found, OR warnings found in `--strict` mode
- 2 – Tool error (git/API failure)

## Project Structure
```
diffaid/
├── diffaid/
│   ├── ai/           # AI engine implementations
│   ├── cli.py        # Command-line interface
│   ├── git.py        # Git integration
│   └── models.py     # Data models
├── tests/            # Test suite
├── pyproject.toml    # Project configuration
└── README.md
```

## Development
### Running Tests

#### Install dev dependencies
```
pip install -e ".[dev]"
```
#### Run tests
```
pytest
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
MIT License – see the LICENSE file for details.

## Acknowledgments
Powered by Google Gemini
