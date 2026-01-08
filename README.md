# DiffAid
[![PyPI version](https://img.shields.io/pypi/v/diffaid)](https://pypi.org/project/diffaid/)
[![Python versions](https://img.shields.io/pypi/pyversions/diffaid)](https://pypi.org/project/diffaid/)
[![License](https://img.shields.io/pypi/l/diffaid)](https://github.com/natetowsley/diffaid/blob/master/LICENSE)

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
Setup
1. Get a free Gemini API key at: https://aistudio.google.com/apikey

2. Set the GEMINI_API_KEY environment variable.

### Mac / Linux:
```
export GEMINI_API_KEY="your-key-here"
```

### Windows (PowerShell):
```
$env:GEMINI_API_KEY="your-key-here"
```
### Permanent Setup

### Mac / Linux
Add to ~/.bashrc or ~/.zshrc:
```
echo 'export GEMINI_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### Windows
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

## Example Output
```
Summary: Added user authentication with JWT tokens

ERROR: Hardcoded secret key detected
  → auth.py 15-17

WARNING: Missing error handling for database connection
  → db.py 42

NOTE: Consider adding rate limiting to login endpoint
  → routes.py 28

---
Found: 1 error, 1 warning, 1 note
```
## Exit Codes

DiffAid uses standard exit codes for CI/CD integration:

- 0 – No errors found (warnings are OK)

- 1 – Errors found

- 2 – Tool error (git/API failure)

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

## Requirements

- Python 3.10+
- Git
- Gemini API key (free tier available)

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
MIT License – see the LICENSE file for details.

## Acknowledgments
Powered by Google Gemini
