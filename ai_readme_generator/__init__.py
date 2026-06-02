"""ai-readme-generator - Generate README from code analysis."""

import os, sys
from pathlib import Path
try:
    import httpx, typer
    from rich.console import Console
except ImportError:
    print("Missing: pip install httpx typer rich"); sys.exit(1)

app = typer.Typer()
console = Console()
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")

PROMPT = """Generate a README.md for the following project codebase.

Include:
## Project Name
## Description
## Features
## Installation
## Usage
## Configuration
## Project Structure
## License

CODE:
{code}"""


def scan_codebase(path: Path) -> str:
    files = []
    for ext in [".py", ".go", ".rs", ".js", ".ts", ".java", ".c", ".h", ".yaml", ".toml", ".json"]:
        for f in path.rglob(f"*{ext}"):
            if ".git" in f.parts or "__pycache__" in f.parts or "node_modules" in f.parts:
                continue
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")[:2000]
                if content.strip():
                    rel = f.relative_to(path)
                    files.append(f"### {rel}\n```\n{content}\n```")
            except Exception:
                pass
    return "\n\n".join(files[:10])


def query_ollama(prompt: str) -> str:
    try:
        with httpx.Client(timeout=120) as client:
            resp = client.post(f"{OLLAMA_HOST}/api/generate", json={
                "model": OLLAMA_MODEL, "prompt": prompt,
                "stream": False, "options": {"temperature": 0.3}
            })
            resp.raise_for_status()
            return resp.json().get("response", "")
    except httpx.HTTPError as e:
        console.print(f"[red]Error: {e}[/]"); sys.exit(1)


@app.command()
def generate(
    path: str = typer.Argument(".", help="Project directory"),
    model: str = typer.Option(OLLAMA_MODEL, "--model", "-m"),
    output: str = typer.Option("README.md", "--output", "-o"),
) -> None:
    project_path = Path(path).resolve()
    if not project_path.is_dir():
        console.print(f"[red]Directory not found:[/] {path}"); sys.exit(1)
    console.print(f"[cyan]Scanning {project_path}...[/]")
    code = scan_codebase(project_path)
    if not code:
        console.print("[yellow]No code files found[/]"); sys.exit(1)
    console.print(f"[cyan]Generating README using {model}...[/]")
    result = query_ollama(PROMPT.format(code=code[:8000]))
    output_path = Path(output)
    output_path.write_text(result)
    console.print(f"[green]README saved to:[/] {output_path}")

if __name__ == "__main__":
    app()
