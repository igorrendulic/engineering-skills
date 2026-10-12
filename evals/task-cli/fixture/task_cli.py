"""A tiny persistent task list. Run with --help for usage."""

import argparse
import json
from pathlib import Path


def load_tasks(path):
    return json.loads(path.read_text()) if path.exists() else []


def save_tasks(path, tasks):
    path.write_text(json.dumps(tasks, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, default=Path("tasks.json"))
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add")
    add.add_argument("title")
    commands.add_parser("list")
    args = parser.parse_args()
    tasks = load_tasks(args.file)
    if args.command == "add":
        task_id = max((task["id"] for task in tasks), default=0) + 1
        tasks.append({"id": task_id, "title": args.title, "done": False})
        save_tasks(args.file, tasks)
        print(task_id)
    else:
        for task in tasks:
            print(f"{task['id']} [{'x' if task['done'] else ' '}] {task['title']}")


if __name__ == "__main__":
    main()
