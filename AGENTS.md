# agentcore-iam-script

This is a Python project using `uv` for dependency management.

## Project Structure

- `main.py` - Main entry point
- `log.py` - Logging utilities (debug, info, warn, error functions)
- `pyproject.toml` - Project metadata and dependencies
- `uv.lock` - Locked dependency versions
- `Makefile` - Development commands
- `.env` - Environment variables (not committed to git)

## Adding Dependencies

To add a new package:
```bash
make install <package-name>
```

## Running the Project

```bash
make start
```

This automatically:
- Loads environment variables from `.env` if present
- Runs the project in the virtual environment

## Available Commands

- `make init` - Initialize project (first time setup)
- `make install` - Install all dependencies
- `make install <package>` - Add a new package
- `make start` - Run the project

## Python Version

This project requires Python 3.13 or higher (see `pyproject.toml`).
