import os
import subprocess
import tempfile
import unittest
from pathlib import Path


INSTALLER = Path(__file__).resolve().parents[1] / "install.sh"
REPOSITORY = "https://github.com/igorrendulic/engineering-skills.git"


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="skills-install-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.source = self.root / "source"
        self.target = self.root / "skills with spaces" / "engineering-skills"
        self.env = dict(os.environ, GIT_CONFIG_GLOBAL=str(self.root / "gitconfig"),
                        GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0")
        self.git("config", "--global", "user.name", "Installer Test")
        self.git("config", "--global", "user.email", "test@example.invalid")
        self.git("config", "--global", "commit.gpgsign", "false")
        # Exercise real Git without contacting GitHub or touching user config.
        self.git("config", "--global", f"url.{self.source}.insteadOf", REPOSITORY)
        self.git("init", "-b", "master", self.source)
        for name in ("SKILL.md", "skills/plan/SKILL.md", "references/plan-lifecycle.md"):
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("initial\n")
        self.commit(self.source)

    def git(self, *args):
        return subprocess.run(["git", *map(str, args)], env=self.env,
                              check=True, capture_output=True, text=True).stdout.strip()

    def commit(self, repo):
        self.git("-C", repo, "add", ".")
        self.git("-C", repo, "commit", "-m", "Fixture change")

    def install(self, success=True, destination=None):
        result = subprocess.run(["sh", str(INSTALLER), str(destination or self.target)],
                                env=self.env, capture_output=True, text=True)
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
        return result

    def test_install_repeat_and_update_preserve_bundle_layout(self):
        self.install()
        self.install()
        (self.source / "SKILL.md").write_text("updated\n")
        self.commit(self.source)
        self.install()
        self.assertEqual((self.target / "SKILL.md").read_text(), "updated\n")
        self.assertTrue((self.target / "skills/plan/SKILL.md").is_file())
        self.assertTrue((self.target / "references/plan-lifecycle.md").is_file())

    def test_existing_non_repository_is_preserved(self):
        self.target.mkdir(parents=True)
        sentinel = self.target / "keep"
        sentinel.write_text("user content")
        self.assertIn("not a Git checkout", self.install(False).stderr)
        self.assertEqual(sentinel.read_text(), "user content")

    def test_local_changes_are_preserved(self):
        self.install()
        for name in ("SKILL.md", "untracked.txt"):
            with self.subTest(name=name):
                self.git("-C", self.target, "restore", "SKILL.md")
                (self.target / name).write_text("user content")
                self.assertIn("local changes", self.install(False).stderr)
                self.assertEqual((self.target / name).read_text(), "user content")

    def test_wrong_repository_is_not_updated(self):
        self.install()
        self.git("-C", self.target, "remote", "set-url", "origin", str(self.source))
        self.assertIn("different repository", self.install(False).stderr)

    def test_ignored_files_are_preserved_when_upstream_starts_tracking_them(self):
        (self.source / ".gitignore").write_text("local.txt\n")
        self.commit(self.source)
        self.install()
        (self.target / "local.txt").write_text("user content")
        (self.source / "local.txt").write_text("upstream content")
        self.git("-C", self.source, "add", "-f", "local.txt")
        self.commit(self.source)
        self.install(False)
        self.assertEqual((self.target / "local.txt").read_text(), "user content")

    def test_divergent_history_is_not_reset(self):
        self.install()
        (self.target / "local.txt").write_text("local commit")
        self.commit(self.target)
        head = self.git("-C", self.target, "rev-parse", "HEAD")
        (self.source / "remote.txt").write_text("remote commit")
        self.commit(self.source)
        self.install(False)
        self.assertEqual(self.git("-C", self.target, "rev-parse", "HEAD"), head)

    def test_feature_branch_is_not_updated(self):
        self.install()
        self.git("-C", self.target, "checkout", "-b", "local-work")
        self.assertIn("master branch", self.install(False).stderr)
        self.assertEqual(self.git("-C", self.target, "branch", "--show-current"), "local-work")

    def test_symlink_is_preserved(self):
        self.target.parent.mkdir(parents=True)
        self.target.symlink_to(self.source, target_is_directory=True)
        self.assertIn("symlink", self.install(False).stderr)
        self.assertTrue(self.target.is_symlink())

    def test_symlink_with_trailing_slashes_or_dots_is_preserved(self):
        self.install()
        alias = self.root / "alias"
        alias.symlink_to(self.target, target_is_directory=True)
        (self.source / "SKILL.md").write_text("updated\n")
        self.commit(self.source)
        for suffix in ("///", "/.", "/././"):
            with self.subTest(suffix=suffix):
                self.assertIn("symlink", self.install(False, str(alias) + suffix).stderr)
                self.assertEqual((self.target / "SKILL.md").read_text(), "initial\n")


if __name__ == "__main__":
    unittest.main()
