import typer
from rich.console import Console
from diffaid.git import get_staged_diff
from diffaid.ai.gemini import GeminiEngine

app = typer.Typer()
console = Console()

@app.command()
def check():
    # Retrieve staged git changes
    diff = get_staged_diff()

    if not diff:
        console.print("[green]No staged changes detected.[/green]")
        raise typer.Exit(0)
    
    try:
        engine = GeminiEngine()
        result = engine.review(diff)
    except RuntimeError as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(1)

    console.print(f"\n[bold]Summary:[/bold] {result.summary}\n\n---\n")

    has_errors = False
    has_warnings = False

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

    if has_errors:
        raise typer.Exit(1)
    if has_warnings:
        raise typer.Exit(2)
    raise typer.Exit(0)
