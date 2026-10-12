import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ExistingBehavior(unittest.TestCase):
    def test_add_and_list(self):
        with tempfile.TemporaryDirectory() as directory:
            command = [sys.executable, str(Path(__file__).with_name("task_cli.py")),
                       "--file", str(Path(directory) / "tasks.json")]
            added = subprocess.run(command + ["add", "Buy milk"], capture_output=True, text=True)
            self.assertEqual(added.returncode, 0, added.stderr)
            self.assertEqual(added.stdout, "1\n")
            listed = subprocess.run(command + ["list"], capture_output=True, text=True)
            self.assertEqual(listed.returncode, 0, listed.stderr)
            self.assertEqual(listed.stdout, "1 [ ] Buy milk\n")


if __name__ == "__main__":
    unittest.main()
