#!/usr/bin/env python3
"""Install and inspect the local plugin without credentials or model inference."""
import argparse
import json
import os
import queue
import shutil
import subprocess
import tempfile
import threading
import time
from pathlib import Path

from test_package import ROOT, WORKFLOWS, check_package, copy_package


def install_package(package, scratch):
    codex = shutil.which("codex")
    if not codex:
        raise RuntimeError("Codex CLI is required for the plugin smoke check")
    check_package(package)
    source, home, project = (scratch / name for name in ("marketplace", "home", "project"))
    copy_package(package, source)
    (home / ".codex").mkdir(parents=True)
    project.mkdir()
    # Only these child processes use the disposable home; no credentials copied.
    env = {key: os.environ[key] for key in ("PATH", "LANG", "LC_ALL", "TERM") if key in os.environ}
    env.update(HOME=str(home), CODEX_HOME=str(home / ".codex"),
               GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0")

    def command(*args):
        result = subprocess.run([codex, *args], cwd=project, env=env, capture_output=True,
                                text=True, timeout=30)
        if result.returncode:
            raise RuntimeError(f"codex {' '.join(args)} failed:\n{result.stderr}\n{result.stdout}")
        return json.loads(result.stdout)

    command("plugin", "marketplace", "add", str(source), "--json")
    result = command("plugin", "add", "engineering-skills@engineering-skills", "--json")
    installed = Path(result["installedPath"]).resolve()
    assert installed.is_relative_to(home.resolve()), "Install escaped disposable home"
    check_package(installed)
    return codex, env, project, installed


def list_skills(codex, env, project):
    with tempfile.TemporaryFile(mode="w+") as errors:
        process = subprocess.Popen([codex, "app-server", "--stdio"], cwd=project, env=env,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=errors, text=True)
        messages = queue.Queue()

        def read_output():
            for line in process.stdout:
                messages.put(line)
            messages.put(None)

        reader = threading.Thread(target=read_output, daemon=True)
        reader.start()

        def send(message):
            process.stdin.write(json.dumps(message) + "\n")
            process.stdin.flush()

        def receive(request_id):
            deadline = time.monotonic() + 20
            while True:
                try:
                    line = messages.get(timeout=max(0, deadline - time.monotonic()))
                except queue.Empty:
                    raise TimeoutError(f"App-server request {request_id} timed out") from None
                if line is None:
                    errors.seek(0)
                    raise RuntimeError(f"App-server closed unexpectedly: {errors.read()}")
                message = json.loads(line)
                if message.get("id") == request_id:
                    if "error" in message:
                        raise RuntimeError(str(message["error"]))
                    return message["result"]

        try:
            send({"id": 1, "method": "initialize", "params": {
                "clientInfo": {"name": "engineering-skills-smoke", "version": "0.1.0"}}})
            receive(1)
            send({"method": "initialized", "params": {}})
            send({"id": 2, "method": "skills/list", "params": {
                "cwds": [str(project)], "forceReload": True}})
            return receive(2)
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
            reader.join(timeout=2)
            process.stdin.close()
            process.stdout.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, default=ROOT)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="engineering-plugin-smoke-") as directory:
        codex, env, project, installed = install_package(args.package.resolve(), Path(directory))
        result = list_skills(codex, env, project)
        listing, = result["data"]
        assert not listing["errors"], listing["errors"]
        plugin_id = "engineering-skills@engineering-skills"
        skills = [skill for skill in listing["skills"] if skill.get("pluginId") == plugin_id]
        expected = {f"engineering-skills:{name}" for name in WORKFLOWS}
        assert len(skills) == len(expected) and {skill["name"] for skill in skills} == expected, skills
        for skill in skills:
            assert skill["enabled"], skill
            assert Path(skill["path"]).resolve().is_relative_to(installed), skill
        # Catch accidental unqualified discovery as well as incorrect ownership.
        owned_paths = [skill for skill in listing["skills"]
                       if Path(skill["path"]).resolve().is_relative_to(installed)]
        assert len(owned_paths) == len(expected), owned_paths
        print("PASS: installed package, internal references, and seven namespaced skills")
        print("\n".join(sorted(expected)))


if __name__ == "__main__":
    main()
