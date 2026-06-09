# AI README Generator

AI-powered README generator that creates comprehensive project documentation from code analysis, using local LLMs via Ollama.

## Features

- Scans project codebase (Python, Go, Rust, JS/TS, Java, C/C++, YAML, TOML, JSON)
- Uses Ollama models (default: `llama3.2`) to generate contextual READMEs
- Customizable via `--model` flag or `OLLAMA_MODEL` env var
- Structured output with Installation, Usage, Configuration, and Project Structure sections
- Ignores `.git`, `__pycache__`, and `node_modules` automatically

## Requirements

- Python 3.10+
- [Ollama](https://ollama.ai) running locally (default: `http://localhost:11434`)
- A pulled model (default: `llama3.2`)

## Installation

```bash
pip install httpx typer rich
pip install -e .
```

## Usage

### Basic

```bash
airg generate
```

### Specify project directory

```bash
airg generate /path/to/project
```

### Use a different model

```bash
airg generate --model llama3.1:70b
```

### Custom output file

```bash
airg generate -o DOCS.md
```

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `llama3.2` | Model for generation |

## How It Works

1. Scans the project directory for code files (up to 10 files, 2000 chars each)
2. Sends the code context to Ollama with a structured prompt
3. Saves the generated README.md to the project directory

## Project Structure

```
ai-readme-generator/
├── ai_readme_generator/
│   └── __init__.py       # CLI entry point and core logic
├── tests/                # Test suite
├── pyproject.toml        # Project configuration
├── README.md
└── LICENSE
```

## License

<br/>

---

<h3 align="center">🐍 Part of the <a href="https://github.com/Raphasha27">Raphasha27</a> Ecosystem</h3>

<p align="center">
  <a href="https://github.com/Raphasha27/Raphasha27">
    <img src="https://img.shields.io/badge/Back_to_Profile-0D1117?style=for-the-badge&logo=github&logoColor=white" />
  </a>
  &nbsp;
  <a href="https://raphasha27.github.io/Raphasha27/ai-snake-game/">
    <img src="https://img.shields.io/badge/▶_Play_AI_Snake-0EA5E9?style=for-the-badge&logo=javascript&logoColor=white" />
  </a>
</p>

MIT

