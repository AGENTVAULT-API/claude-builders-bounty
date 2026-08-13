import importlib.machinery
import importlib.util
from pathlib import Path
import sys


SCRIPT = Path(__file__).parents[1] / "claude-review"
loader = importlib.machinery.SourceFileLoader("claude_review", str(SCRIPT))
spec = importlib.util.spec_from_loader(loader.name, loader)
module = importlib.util.module_from_spec(spec)
sys.modules[loader.name] = module
loader.exec_module(module)


def test_parse_and_review_are_deterministic():
    diff = """diff --git a/app.py b/app.py
--- a/app.py
+++ b/app.py
@@ -1 +1 @@
-print('old')
+print('new')
diff --git a/tests/test_app.py b/tests/test_app.py
--- /dev/null
+++ b/tests/test_app.py
@@ -0,0 +1 @@
+assert True
"""
    stats = module.parse_diff(diff)
    output = module.review({"title": "Change output"}, stats)

    assert stats.files == ["app.py", "tests/test_app.py"]
    assert stats.additions == 2
    assert stats.deletions == 1
    assert "## Summary" in output
    assert "## Risks" in output
    assert "## Suggestions" in output
    assert "## Confidence\n\n**High**" in output
    assert output == module.review({"title": "Change output"}, stats)


def test_uncovered_large_diff_reports_risks():
    stats = module.DiffStats(files=["src/auth/session.py"], additions=501)
    output = module.review({"title": "Sessions"}, stats)

    assert "No test changes" in output
    assert "large patch size" in output
    assert "Security- or payment-sensitive" in output
    assert output.endswith("**Medium**\n")
