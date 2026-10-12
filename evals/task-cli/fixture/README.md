# Task CLI

A personal task list implemented with Python 3.11+ and the standard library.
`task_cli.py` owns argument parsing, persistence, and display; keep this small
application dependency-free. `test_task_cli.py` contains its unittest tests.

```sh
python3 task_cli.py --file tasks.json add "Buy milk"
python3 task_cli.py --file tasks.json list
python3 -m unittest discover -v
```

Storage is a JSON array of objects with integer `id`, string `title`, and boolean
`done`. Preserve extra fields if present. IDs identify records, not array positions.
Listing prints `<id> [ ] <title>` for pending tasks and `<id> [x] <title>` for
completed tasks. Keep insertion order. Adding prints the newly assigned ID.

This README is the authoritative project document. There is no separate
architecture document, formatter, linter, type checker, or build step.
