"""Apply a reference solution to a disposable fixture; never used by the agent."""
from pathlib import Path


def apply(project: Path):
    path = project / "task_cli.py"
    source = path.read_text().replace(
        '    commands.add_parser("list")',
        '    commands.add_parser("list")\n'
        '    done = commands.add_parser("done")\n'
        '    done.add_argument("id", type=int)',
    ).replace(
        '    if args.command == "add":',
        '''    if args.command == "done":
        if args.id <= 0:
            parser.error("ID must be positive")
        task = next((task for task in tasks if task["id"] == args.id), None)
        if task is None:
            parser.error("unknown task ID")
        if not task["done"]:
            task["done"] = True
            save_tasks(args.file, tasks)
    elif args.command == "add":''',
    )
    path.write_text(source)
