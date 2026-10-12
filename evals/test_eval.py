import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from grade import grade, grading_environment
from run import execute, git, git_state, native_reviews, snapshot

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("oracle", HERE / "task-cli/oracle.py")
oracle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)


class GraderTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.project = Path(self.directory.name) / "project"
        shutil.copytree(HERE / "task-cli/fixture", self.project)

    def test_starting_project_is_not_a_solution(self):
        checks = grade(self.project)
        self.assertTrue(checks[0]["passed"])
        self.assertFalse(checks[1]["passed"])

    def test_reference_passes_both_variants(self):
        oracle.apply(self.project)
        for variant in ("standard", "sparse-ids"):
            with self.subTest(variant=variant):
                checks = grade(self.project, variant)
                self.assertTrue(all(check["passed"] for check in checks), checks)

    def test_grading_accepts_a_relative_project_path(self):
        oracle.apply(self.project)
        original = Path.cwd()
        try:
            os.chdir(self.project.parent)
            checks = grade(Path("project"))
        finally:
            os.chdir(original)
        self.assertTrue(all(check["passed"] for check in checks), checks)

    def test_grader_rejects_rewriting_completed_task(self):
        oracle.apply(self.project)
        source = self.project / "task_cli.py"
        source.write_text(source.read_text().replace('if not task["done"]:', 'if True:'))
        checks = {check["name"]: check["passed"] for check in grade(self.project)}
        self.assertFalse(checks["idempotent without writes"])

    def test_grader_rejects_position_instead_of_id(self):
        oracle.apply(self.project)
        source = self.project / "task_cli.py"
        source.write_text(source.read_text().replace(
            'next((task for task in tasks if task["id"] == args.id), None)',
            'tasks[args.id - 1] if 0 < args.id <= len(tasks) else None',
        ))
        checks = grade(self.project, "sparse-ids")
        self.assertFalse(checks[1]["passed"])

    def test_grader_rejects_always_completing_first_task(self):
        oracle.apply(self.project)
        source = self.project / "task_cli.py"
        source.write_text(source.read_text().replace(
            'task["done"] = True', 'tasks[0]["done"] = True',
        ))
        for variant in ("standard", "sparse-ids"):
            checks = grade(self.project, variant)
            self.assertFalse(checks[1]["passed"], variant)

    def test_grader_rejects_dropping_completed_record_metadata(self):
        oracle.apply(self.project)
        source = self.project / "task_cli.py"
        source.write_text(source.read_text().replace(
            'task["done"] = True', 'task.pop("metadata", None)\n            task["done"] = True',
        ))
        self.assertFalse(grade(self.project)[1]["passed"])

    def test_grader_rejects_add_replacing_existing_records(self):
        oracle.apply(self.project)
        source = self.project / "task_cli.py"
        source.write_text(source.read_text().replace(
            'tasks.append({"id": task_id, "title": args.title, "done": False})',
            'tasks = [{"id": task_id, "title": args.title, "done": False}]',
        ))
        for variant in ("standard", "sparse-ids"):
            checks = {check["name"]: check["passed"] for check in grade(self.project, variant)}
            self.assertFalse(checks["add preserves existing completed and pending records"])

    def test_description_only_git_checks_detect_staging_and_branch_change(self):
        git(self.project, "init", "-b", "master")
        git(self.project, "add", ".")
        git(self.project, "-c", "user.name=Eval", "-c", "user.email=eval@localhost", "commit", "-m", "Fixture")
        (self.project / "NOTES.txt").write_text("Unstaged change\n")
        files = snapshot(self.project)
        state = git_state(self.project)
        git(self.project, "add", "NOTES.txt")
        self.assertEqual(files, snapshot(self.project))
        self.assertNotEqual(state, git_state(self.project))
        state = git_state(self.project)
        git(self.project, "checkout", "-b", "other")
        self.assertNotEqual(state, git_state(self.project))

    def test_grading_does_not_inherit_credentials(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-secret", "CODEX_API_KEY": "test-secret",
                                    "CODEX_HOME": "/private/auth", "GH_TOKEN": "test-secret"}):
            environment = grading_environment(self.directory.name)
        self.assertFalse({"OPENAI_API_KEY", "CODEX_API_KEY", "CODEX_HOME", "GH_TOKEN"} & environment.keys())
        self.assertEqual(environment["HOME"], self.directory.name)

    def test_timeout_stops_descendant_process(self):
        marker = Path(self.directory.name) / "child-survived"
        child = f"import time; from pathlib import Path; time.sleep(1); Path({str(marker)!r}).touch()"
        parent = f"import subprocess, sys, time; subprocess.Popen([sys.executable, '-c', {child!r}]); time.sleep(10)"
        with self.assertRaises(subprocess.TimeoutExpired):
            execute([sys.executable, "-c", parent], "", self.project, dict(os.environ),
                    Path(self.directory.name) / "timeout", 0.3)
        time.sleep(1)
        self.assertFalse(marker.exists(), "timed-out agent left a child running")

    def test_implementer_claim_does_not_count_as_native_review(self):
        home = Path(self.directory.name)
        sessions = home / "sessions"
        sessions.mkdir()
        result = {"findings": [], "overall_correctness": "patch is correct"}
        events = [{"type": "session_meta", "payload": {"source": "exec"}},
                  {"type": "event_msg", "payload": {"type": "task_complete",
                   "last_agent_message": json.dumps(result), "completed_at": 1}}]
        path = sessions / "review.jsonl"
        path.write_text("\n".join(json.dumps(event) for event in events))
        self.assertEqual(native_reviews(home), [])
        events[0]["payload"]["source"] = {"subagent": "review"}
        path.write_text("\n".join(json.dumps(event) for event in events))
        self.assertEqual(native_reviews(home)[0]["verdict"], result)

    def test_timeout_stops_sigterm_ignoring_descendant(self):
        marker = Path(self.directory.name) / "child-survived"
        ready = Path(self.directory.name) / "ready"
        child = ("import signal, time; from pathlib import Path; "
                 "signal.signal(signal.SIGTERM, signal.SIG_IGN); "
                 f"Path({str(ready)!r}).touch(); time.sleep(1); Path({str(marker)!r}).touch()")
        parent = f"import subprocess, sys, time; subprocess.Popen([sys.executable, '-c', {child!r}]); time.sleep(10)"
        with self.assertRaises(subprocess.TimeoutExpired):
            execute([sys.executable, "-c", parent], "", self.project, dict(os.environ),
                    Path(self.directory.name) / "timeout", 0.3)
        self.assertTrue(ready.exists(), "child did not start before timeout")
        time.sleep(1)
        self.assertFalse(marker.exists(), "descendant survived after its process leader exited")


if __name__ == "__main__":
    unittest.main()
