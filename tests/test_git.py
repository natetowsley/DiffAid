import pytest
from unittest.mock import patch, Mock
import subprocess
from diffaid.git import get_staged_diff

def test_get_staged_diff_success(sample_diff):
    """Test successful git diff retrieval"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = Mock(stdout=sample_diff)
        result = get_staged_diff()
        assert result == sample_diff
        mock_run.assert_called_once_with(
            ["git", "diff", "--staged"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

def test_get_staged_diff_no_git():
    """Test error when git is not installed"""
    with patch('shutil.which', return_value=None):
        with pytest.raises(RuntimeError, match="Git is not installed"):
            get_staged_diff()

def test_get_staged_diff_empty():
    """Test empty diff (no staged changes)"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = Mock(stdout="")
        result = get_staged_diff()
        assert result == ""
