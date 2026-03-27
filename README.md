# AgenticAI

A command-line AI coding agent built in Python using the Google Gemini API — a toy implementation of tools like Claude Code or Cursor's Agent Mode. The agent autonomously reasons, selects tools, and iterates in a feedback loop to find and fix bugs in real projects.

---

## What It Does

You give the agent a task in plain English. It figures out what to do.

```bash
uv run main.py "fix my calculator app, it's not starting correctly"
```

```
# Calling function: get_files_info
# Calling function: get_file_content
# Calling function: write_file
# Calling function: run_python_file
# Calling function: write_file
# Calling function: run_python_file
# Final response:
# The calculator app is now working correctly.
```

The agent reads the file system, understands the bug, rewrites the file, runs it, and verifies the fix — all on its own.

---

## How It Works

At its core, an AI agent is just an LLM running in a loop with tools it can call. That's it.

```
User prompt
    ↓
Gemini reasons about what to do
    ↓
Gemini calls a tool (e.g. get_file_content)
    ↓
Tool result is returned to Gemini
    ↓
Gemini reasons about the result
    ↓
Repeat until task is complete
    ↓
Final response returned to user
```

The magic isn't in the model — it's in the loop and the tools. This project implements that loop from scratch using Gemini's function calling API.

---

## Project Structure

```
AgenticAI/
├── main.py                  # Entry point + agentic loop
├── functions/
│   ├── get_files_info.py    # List directory contents
│   ├── get_file_content.py  # Read a file (up to 10,000 chars)
│   ├── write_file.py        # Write or overwrite a file
│   └── run_python_file.py   # Execute a Python file and capture output
├── calculator/              # Sample buggy project for the agent to fix
├── .env                     # API key (not committed)
└── pyproject.toml
```

---

## Tools

Each tool is a sandboxed Python function registered with the Gemini API via function calling. The agent selects which tools to call based on the task.

| Tool | What it does |
|------|-------------|
| `get_files_info` | Lists files and directories at a given path, including name, size, and type |
| `get_file_content` | Reads up to 10,000 characters from a file, with a truncation notice if the file is larger |
| `write_file` | Creates or overwrites a file at a given path, creating any missing parent directories |
| `run_python_file` | Executes a Python file and returns stdout/stderr |

### The Sandbox Pattern

Every tool enforces the same security constraint: the LLM can only access files within the developer-defined `working_directory`. This is validated using `os.path.commonpath()`:

```python
abs_working_dir = os.path.abspath(working_directory)
abs_target = os.path.abspath(os.path.join(abs_working_dir, path_from_llm))

if os.path.commonpath([abs_working_dir, abs_target]) != abs_working_dir:
    return f'Error: Cannot access "{path_from_llm}" as it is outside the permitted working directory'
```

This prevents the LLM from escaping the sandbox via path traversal (e.g., `../../etc/passwd`).

### Error Handling Design

All tools return error messages as strings rather than raising exceptions. This is intentional — it lets the agent read the error, reason about it, and decide how to recover, rather than crashing the program.

---

## Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

### Installation

```bash
git clone https://github.com/yourusername/AgenticAI.git
cd AgenticAI
uv sync
```

### Configuration

Create a `.env` file in the root directory:

```
GEMINI_API_KEY=your_api_key_here
```

### Usage

```bash
uv run main.py "your task here"
```

Use the `--verbose` flag to see tool calls printed to the console:

```bash
uv run main.py "what files are in the root?" --verbose
```

---

## Key Concepts

- **LLM function calling** — registering Python functions as tools the model can invoke
- **The agentic loop** — feeding tool results back into the model and iterating until a task is complete
- **Sandboxing** — restricting an LLM's file system access using path validation
- **Token awareness** — monitoring prompt and response token counts to stay within API limits
- **Robust tool design** — returning errors as strings so the agent can self-correct

