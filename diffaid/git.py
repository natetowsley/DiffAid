import subprocess
import shutil

def get_staged_diff() -> str:
    """
    Retrieve the staged git diff
    
    Returns: 
        str: The staged diff output from git

    Raises: 
        Runtime Error: If git is not available or command fails
    """
    # Check if git is installed and available
    if not shutil.which("git"):
        raise RuntimeError(
            "[red]Git is not installed or not in PATH[/red]"
        )
    # Using subprocess to run 'git diff --staged'
    try:
        result = subprocess.run(
            ["git", "diff", "--staged"],
            # Captures output rather than printing to terminal
            capture_output=True,
            # Makes output strings rather than bytes
            text=True,
            encoding="utf-8"
        )
        return result.stdout.strip()
    # Handle failed git diff (not a git repository, permission issues, etc)
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            f"Git command failed: {error.stderr or 'Unknown error'}"
        ) from error
