# calculator

A small command-line calculator: evaluates a whitespace-separated infix
expression with `+ - * /` and standard operator precedence.

```bash
uv run main.py "3 + 4 * 2"
```

This project is also the sandbox the AI agent in the parent [aiagent](../README.md)
project operates in — it's the directory the agent's tools (`get_files_info`,
`get_file_content`, `write_file`, `run_python_file`) are restricted to.
