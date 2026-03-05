# FastAPI Starter Kit

A minimal FastAPI boilerplate with a clean project structure, health-check endpoint, and quality tooling pre-configured.

## Project Structure

```
fastapi-starter-kit/
├── app/
│   ├── __init__.py
│   └── main.py              # FastAPI application & health endpoint
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Shared pytest fixtures
│   └── test_main.py          # Test cases
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Dev / testing dependencies
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12+

### Setup

```bash
# Clone the repository
git clone <repo-url> && cd fastapi-starter-kit

# Create & activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install all dependencies (production + dev)
pip install -r requirements-dev.txt
```

### Run the Server

```bash
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger Docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Path | Description  |
| ------ | ---- | ------------ |
| `GET`  | `/`  | Health check |

## Quality Tooling

All tools are included in `requirements-dev.txt`:

| Tool       | Purpose          | Command                              |
| ---------- | ---------------- | ------------------------------------ |
| **Black**  | Code formatting  | `black --check app/ tests/`          |
| **isort**  | Import ordering  | `isort --check-only --diff app/ tests/` |
| **Pylint** | Code quality     | `pylint app/ tests/`                 |
| **mypy**   | Type checking    | `mypy app/ tests/`                   |
| **pytest** | Unit tests       | `pytest tests/ -v`                   |

### Run All Checks

```bash
black --check app/ tests/ && \
isort --check-only --diff app/ tests/ && \
pylint app/ tests/ && \
mypy app/ tests/ && \
pytest tests/ -v
```

## License

MIT
