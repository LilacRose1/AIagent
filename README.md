# aiagent

A small command-line AI coding agent. It sends your prompt to an LLM (via
[OpenRouter](https://openrouter.ai)) along with a set of tools, and lets the
model call those tools — listing files, reading files, writing files, and
running Python scripts — inside a sandboxed working directory until it can
give you a final answer.

The included sandbox is a toy `calculator/` project (an infix expression
evaluator) that the agent can inspect, edit, and test.

## How it works

1. `main.py` builds a message list (system prompt + your prompt) and sends it
   to the model, along with the tool schemas from `call_function.py`.
2. If the model responds with tool calls, `call_function.py` dispatches each
   one to the matching function in `functions/`, injects the fixed working
   directory (`./calculator`), and feeds the result back to the model.
3. This repeats (up to 20 rounds) until the model responds with plain text
   instead of a tool call, which is printed as the final answer.

## Tools available to the agent

| Function | Purpose |
|---|---|
| `get_files_info` | List files/directories with size and type |
| `get_file_content` | Read a file's content (truncated at 10,000 characters) |
| `write_file` | Create or overwrite a file with given content |
| `run_python_file` | Run a Python script with optional CLI args |

All four are restricted to the working directory: any path that would
resolve outside it (e.g. via `..`) is rejected before the filesystem is
touched.

## Setup

Requires Python 3.13+ and [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync
```

Create a `.env` file in the project root with your OpenRouter API key:

```
OPENROUTER_API_KEY=your-key-here
```

`.env` is gitignored — never commit your API key.

## Usage

```bash
uv run main.py "your prompt here"
uv run main.py "your prompt here" --verbose   # also prints token usage and tool output
```

Example:

```bash
uv run main.py "fix the bug in the calculator and run its tests to confirm"
```

## Project structure

```
main.py               # entry point: CLI parsing + the agent loop
call_function.py      # dispatches model tool calls to functions/
prompts.py            # system prompt defining the agent's behavior/tools
functions/            # the four sandboxed tools the model can call
calculator/           # sample sandboxed project the agent operates on
```

## Acknowledgments

Built while following [boot.dev](https://www.boot.dev)'s guided "Build an AI
Agent" project. This README was written with the help of AI (Claude).

