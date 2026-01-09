import typer
import json
from rich.console import Console
from diffaid.git import get_staged_diff
from diffaid.ai.gemini import GeminiEngine

app = typer.Typer(
    help="AI-assisted git diff review CLI",
    add_completion=False
)
console = Console()

@app.command()
def check(
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output raw JSON instead of formatted text"
    )
):
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
    try:
        diff = get_staged_diff()
    except RuntimeError as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(2)

    if not diff:
        if json_output:
            print(json.dumps({"message": "No staged changes detected."}))
        else:
            console.print("[green]No staged changes detected.[/green]")
        raise typer.Exit(0)
    
    # Set engine and retrieve AI response
    try:
        engine = GeminiEngine()
        result = engine.review(diff)
    except RuntimeError as error:
        if json_output:
            print(json.dumps({"error": str(error)}))
        else:
            console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(2)
    
    # JSON output mode
    if json_output:
        # Convert Pydantic model to dict, then to JSON
        output = result.model_dump()
        print(json.dumps(output, indent=2))

        # Exit code based on findings
        has_errors = any(f.severity == "error" for f in result.findings)
        raise typer.Exit(1 if has_errors else 0)

    # Diff summary
    console.print(f"\n[bold]Summary:[/bold] {result.summary}\n")
    console.print("\n---\n")

    has_errors = False
    has_warnings = False

    # Finding contents
    if not result.findings:
        console.print("[green]No issues found![/green]\n")
    else:
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
    console.print(f"[bold]Found:[/bold] {counts['error']} error{'s' if counts['error'] != 1 else ''}, "
                  f"{counts['warning']} warning{'s' if counts['warning'] != 1 else ''}, "
                  f"{counts['note']} note{'s' if counts['note'] != 1 else ''}")

    if has_errors:
        raise typer.Exit(1)
    raise typer.Exit(0)
