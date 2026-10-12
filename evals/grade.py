"""Black-box acceptance checks. Run only after the development agent exits."""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def grading_environment(home):
    environment = {key: os.environ[key] for key in ("PATH", "LANG", "LC_ALL") if key in os.environ}
    environment.update(HOME=str(home), TMPDIR=str(home), PYTHONDONTWRITEBYTECODE="1")
    return environment


def grade(project: Path, variant="standard"):
    project = project.resolve()
    checks = []
    with tempfile.TemporaryDirectory(prefix="skill-eval-grading-") as directory:
        store = Path(directory) / "tasks.json"

        def cli(*args):
            return subprocess.run(
                [sys.executable, str(project / "task_cli.py"), "--file", str(store), *args],
                cwd=directory, env=grading_environment(directory), capture_output=True, text=True, timeout=15,
            )

        def check(name, passed, detail=""):
            checks.append({"name": name, "passed": bool(passed), "detail": detail})

        added = cli("add", "Buy milk")
        listed = cli("list")
        check("existing add/list", added.returncode == listed.returncode == 0
              and added.stdout == "1\n" and listed.stdout == "1 [ ] Buy milk\n")
        ids = [1, 2] if variant == "standard" else [41, 7]
        tasks = [{"id": ids[0], "title": "Milk 🥛", "done": False, "tag": "home"},
                 {"id": ids[1], "title": "Read", "done": False, "metadata": {"priority": 2}}]
        store.write_text(json.dumps(tasks) + "\n")
        result = cli("done", str(ids[1]))
        expected = [tasks[0], dict(tasks[1], done=True)]
        try:
            actual = json.loads(store.read_text())
        except (ValueError, OSError):
            actual = None
        check("completion preserves records", result.returncode == 0 and actual == expected,
              result.stderr)
        listed = cli("list")
        check("completion visible across processes", listed.returncode == 0
              and listed.stdout == f"{ids[0]} [ ] Milk 🥛\n{ids[1]} [x] Read\n")
        before = store.read_bytes() if store.exists() else b""
        if store.exists():
            os.utime(store, ns=(1_000_000_000, 1_000_000_000))
        repeated = cli("done", str(ids[1]))
        check("idempotent without writes", repeated.returncode == 0 and store.exists()
              and store.read_bytes() == before and store.stat().st_mtime_ns == 1_000_000_000)
        for task_id in ("999", "abc", "0", "-1", "1.5"):
            result = cli("done", task_id)
            check(f"reject {task_id} without mutation", result.returncode != 0
                  and store.exists() and store.read_bytes() == before)
        next_id = max(ids) + 1
        added = cli("add", "Third")
        listed = cli("list")
        try:
            actual = json.loads(store.read_text())
        except (ValueError, OSError):
            actual = None
        check("add preserves existing completed and pending records",
              added.returncode == listed.returncode == 0 and added.stdout == f"{next_id}\n"
              and actual == expected + [{"id": next_id, "title": "Third", "done": False}]
              and listed.stdout == f"{ids[0]} [ ] Milk 🥛\n{ids[1]} [x] Read\n{next_id} [ ] Third\n")
        store.unlink(missing_ok=True)
        result = cli("done", "1")
        check("missing storage stays absent", result.returncode != 0 and not store.exists())
    return checks
