# Learning

A small collection of practical programming examples and learning notes. Each snippet is intentionally self-contained so it can be read, run, and modified independently.

## Python examples

Run these commands from the repository root with Python 3:

| File | What it demonstrates |
| --- | --- |
| `learning_snippets/0002-python_csv_sums.py` | Sum numeric values by CSV column; read from a file or standard input. |
| `learning_snippets/0005-python_unique_preserve_order.py` | Remove duplicates while keeping first-occurrence order. |
| `learning_snippets/0006-python_count_items.py` | Count occurrences of hashable values. |
| `learning_snippets/0007-python_chunked.py` | Split an iterable into bounded-size lists. |
| `learning_snippets/0008-python_retry_backoff.py` | Retry transient failures with exponential backoff. |
| `learning_snippets/0009-python_asyncio_semaphore.py` | Limit concurrent asynchronous operations. |

The examples with built-in checks can be run directly:

```bash
python3 learning_snippets/0005-python_unique_preserve_order.py
python3 learning_snippets/0006-python_count_items.py
python3 learning_snippets/0007-python_chunked.py
python3 learning_snippets/0008-python_retry_backoff.py
python3 learning_snippets/0009-python_asyncio_semaphore.py
```

For the CSV example, pass a file path or pipe CSV text through standard input:

```bash
python3 learning_snippets/0002-python_csv_sums.py data.csv
cat data.csv | python3 learning_snippets/0002-python_csv_sums.py
```

## Other examples

- `learning_snippets/0001-mini_bash.sh` — print Fibonacci numbers (for example, `bash learning_snippets/0001-mini_bash.sh 10`).
- `learning_snippets/0003-js_debounce.js` — a debounce utility written as an ES module.
- `learning_snippets/0004-go_rate_limiter.go` — a small token-bucket-style rate-limiter demonstration (`go run learning_snippets/0004-go_rate_limiter.go`).
- `sample.py` — a minimal FastAPI sum endpoint. Install FastAPI and Uvicorn, then run `uvicorn sample:app --reload`.
- `king_of_codes.md` — creative coding notes and an example of keeping API keys in environment variables rather than source files.

## Working with the examples

1. Read the docstring or comments first.
2. Run the example and inspect its output.
3. Change one input or edge case and rerun it.
4. Keep credentials and other secrets out of commits.

No single package setup is required for the standalone snippets; install a language runtime or optional dependency only for the example you want to run.
