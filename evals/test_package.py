"""Distribution contracts; no Codex CLI or model calls required."""
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = {"init", "plan", "implementation", "pr-review", "structural-review", "github-pr", "help"}
PACKAGE_FILES = ("plugin.json", ".agents/plugins/marketplace.json", "SKILL.md", "skills", "references")


def copy_package(source, target):
    for name in PACKAGE_FILES:
        src, dst = source / name, target / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copyfile(src, dst)


def check_package(root):
    """Check the actual package and its internal instruction references."""
    root = root.resolve()
    manifest = json.loads((root / "plugin.json").read_text())
    assert manifest["name"] == "engineering-skills", "Wrong plugin namespace"
    assert manifest["$schema"] == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    assert re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]), "Missing release version"
    marketplace = json.loads((root / ".agents/plugins/marketplace.json").read_text())
    assert marketplace["name"] == "engineering-skills"
    entry, = marketplace["plugins"]
    assert entry["name"] == manifest["name"]
    assert entry["source"] == {"source": "local", "path": "./"}
    assert entry["policy"]["installation"] == "AVAILABLE"
    assert entry["policy"]["authentication"] == "ON_INSTALL"
    assert entry["category"] == "Productivity"

    skills = list((root / "skills").glob("*/SKILL.md"))
    assert {path.parent.name for path in skills} == WORKFLOWS, "Missing or unexpected workflow"
    for path in skills:
        name = re.search(r"^name: (.+)$", path.read_text(), re.MULTILINE)
        assert name and name[1] == path.parent.name, f"Invalid short skill name: {path}"
    catalog = dict(re.findall(r"\| `([\w-]+)` \| `([^`]+)` \|", (root / "SKILL.md").read_text()))
    assert catalog == {name: f"skills/{name}/SKILL.md" for name in WORKFLOWS}, "Catalog mismatch"

    for path in [root / "SKILL.md", *(root / "skills").rglob("*.md"), *(root / "references").rglob("*.md")]:
        content = path.read_text()
        links = re.findall(r"\]\(([^\s)]+)\)", content)
        links += re.findall(r"`((?:\.{1,2}/|references/|skills/)[^`\s]+\.md)`", content)
        for link in links:
            if "://" in link or link.startswith("#"):
                continue
            target = (path.parent / link.split("#", 1)[0]).resolve()
            assert target.is_relative_to(root), f"Reference leaves package: {path}: {link}"
            assert target.is_file(), f"Missing reference: {path}: {link}"


class PackageTests(unittest.TestCase):
    def test_package_contract(self):
        check_package(ROOT)

    def test_missing_shared_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory)
            copy_package(ROOT, package)
            (package / "references/plan-lifecycle.md").unlink()
            with self.assertRaisesRegex(AssertionError, "Missing reference"):
                check_package(package)

    def test_wrong_namespace_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory)
            copy_package(ROOT, package)
            manifest_path = package / "plugin.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["name"] = "wrong-name"
            manifest_path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(AssertionError, "Wrong plugin namespace"):
                check_package(package)


if __name__ == "__main__":
    unittest.main()
