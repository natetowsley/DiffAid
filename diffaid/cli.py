import typer
from rich.console import Console
from diffaid.git import get_staged_diff
from diffaid.ai.gemini import GeminiEngine

app = typer.Typer()
console = Console()

@app.command()
def check():
    """
    Review staged git changes with AI.
    
    Analyzes your staged diff and reports errors, warnings, and notes
    about potential issues before you commit.
    
    Example Usage:
    
      # Basic review
      $ diffaid
    
    Exit Codes:
      0 - No errors found
      1 - Errors found, or warnings in strict mode
      2 - Tool error (git failure, API issues)
    """

    # Retrieve staged git changes
    diff = get_staged_diff()

    if not diff:
        console.print("[green]No staged changes detected.[/green]")
        raise typer.Exit(0)
    
    # Set engine and retrieve AI response
    try:
        engine = GeminiEngine()
        result = engine.review(diff)
    except RuntimeError as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(2)

    # Diff summary
    console.print(f"\n[bold]Summary:[/bold] {result.summary}\n\n---\n")

    has_errors = False
    has_warnings = False

    # Finding contents
    for f in result.findings:
        if f.severity == "error":
            has_errors = True
        elif f.severity == "warning":
            has_warnings = True

        color = {"error": "red", "warning": "yellow", "note": "cyan"}[f.severity]
        console.print(f"[{color}]{f.severity.upper()}[/]: {f.message}")
        if f.file:
            console.print(f"[bold]  → {f.file} {f.lines or ''}[/bold]")
        console.print()

    # Count findings
    counts = {"error": 0, "warning": 0, "note": 0}
    for f in result.findings:
        counts[f.severity] += 1
    
    console.print("---\n")
    console.print(f"[bold]Found:[/bold] {counts['error']} errors, "
                  f"{counts['warning']} warnings, {counts['note']} notes")

    if has_errors:
        raise typer.Exit(1)
    if has_warnings:
        raise typer.Exit(0)
    raise typer.Exit(0)
