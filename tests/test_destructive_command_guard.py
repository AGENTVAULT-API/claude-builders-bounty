#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".claude" / "hooks" / "destructive_command_guard.py"


def run(command: str) -> subprocess.CompletedProcess[str]:
    payload = {"tool_name": "Bash", "tool_input": {"command": command}, "cwd": "/tmp/claude-hook-test"}
    return subprocess.run([sys.executable, str(HOOK)], input=json.dumps(payload), text=True, capture_output=True)


def test_allowed_commands_pass() -> None:
    for command in ["git status", "python3 -m pytest", "rm -r build", "DELETE FROM logs WHERE id = 1"]:
        proc = run(command)
        assert proc.returncode == 0, (command, proc.returncode, proc.stderr)


def test_blocked_commands_fail() -> None:
    cases = [
        "rm -rf build",
        "sudo rm -fr /tmp/example",
        "psql -c 'DROP TABLE users'",
        "git push --force origin main",
        "git push -f",
        "git push --force-with-lease",
        "TRUNCATE audit_log",
        "DELETE FROM users;",
        "DELETE FROM users\n",
    ]
    for command in cases:
        proc = run(command)
        assert proc.returncode == 2, (command, proc.returncode, proc.stderr)
        assert "Blocked destructive Bash command" in proc.stderr


if __name__ == "__main__":
    test_allowed_commands_pass()
    test_blocked_commands_fail()
    print("all tests passed")
