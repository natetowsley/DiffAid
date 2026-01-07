import pytest
from typer.testing import CliRunner
from unittest.mock import patch, Mock
from diffaid.cli import app
from diffaid.models import ReviewResult, Finding

runner = CliRunner()

def test_cli_no_staged_changes():
    """Test CLI with no staged changes"""
    with patch('diffaid.cli.get_staged_diff', return_value=""):
        result = runner.invoke(app)
        assert result.exit_code == 0
        assert "No staged changes" in result.stdout

def test_cli_with_errors(sample_diff, set_api_key):
    """Test CLI with error findings"""
    mock_result = ReviewResult(
        summary="Found issues",
        findings=[Finding(severity="error", message="Critical bug")]
    )
    
    with patch('diffaid.cli.get_staged_diff', return_value=sample_diff):
        with patch('diffaid.cli.GeminiEngine') as mock_engine:
            mock_engine.return_value.review.return_value = mock_result
            result = runner.invoke(app)
            
            assert result.exit_code == 1
            assert "ERROR" in result.stdout
            assert "Critical bug" in result.stdout

def test_cli_with_warnings_only(sample_diff, set_api_key):
    """Test CLI with only warnings (should exit 0)"""
    mock_result = ReviewResult(
        summary="Minor issues",
        findings=[Finding(severity="warning", message="Consider refactoring")]
    )
    
    with patch('diffaid.cli.get_staged_diff', return_value=sample_diff):
        with patch('diffaid.cli.GeminiEngine') as mock_engine:
            mock_engine.return_value.review.return_value = mock_result
            result = runner.invoke(app)
            
            assert result.exit_code == 0
            assert "WARNING" in result.stdout

def test_cli_git_error():
    """Test CLI handling of git errors"""
    with patch('diffaid.cli.get_staged_diff', side_effect=RuntimeError("Git failed")):
        result = runner.invoke(app)
        assert result.exit_code == 2
        assert "Error:" in result.stdout

def test_cli_no_issues_found(sample_diff, set_api_key):
    """Test CLI with no issues found"""
    mock_result = ReviewResult(summary="All good", findings=[])
    
    with patch('diffaid.cli.get_staged_diff', return_value=sample_diff):
        with patch('diffaid.cli.GeminiEngine') as mock_engine:
            mock_engine.return_value.review.return_value = mock_result
            result = runner.invoke(app)
            
            assert result.exit_code == 0
            assert "No issues found" in result.stdout