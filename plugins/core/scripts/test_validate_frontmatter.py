"""Tests for validate_frontmatter.py. Run: python3 -m unittest discover -s scripts -p 'test_*.py'"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_frontmatter as v  # noqa: E402


def check(name, body, kind):
    with tempfile.TemporaryDirectory() as t:
        p = Path(t) / name
        p.write_text(body, encoding="utf-8")
        return v.check(p, kind)


def severities(findings):
    return {s for s, _ in findings}


class CommandTest(unittest.TestCase):
    def test_valid_command(self):
        body = "---\ndescription: Does a thing\nallowed-tools:\n  - Read\n---\n\n# Title\n"
        self.assertEqual(check("do-thing.md", body, "commands"), [])

    def test_name_field_is_an_error(self):
        body = "---\nname: x\ndescription: d\nallowed-tools: [Read]\n---\n# T\n"
        self.assertIn("ERROR", severities(check("x.md", body, "commands")))

    def test_missing_allowed_tools_and_description(self):
        findings = check("x.md", "---\ncategory: dev\n---\n# T\n", "commands")
        messages = " ".join(m for _, m in findings)
        self.assertIn("description", messages)
        self.assertIn("allowed-tools", messages)

    def test_no_frontmatter(self):
        self.assertEqual(check("x.md", "# T\n", "commands")[0][0], "ERROR")


class AgentTest(unittest.TestCase):
    GOOD = "---\nname: code-reviewer\ndescription: Reviews code\ncategory: quality\nmodel: sonnet\ncolor: blue\n---\n# R\n"

    def test_valid_agent(self):
        self.assertEqual(check("code-reviewer.md", self.GOOD, "agents"), [])

    def test_full_model_id_is_an_error(self):
        body = self.GOOD.replace("sonnet", "claude-opus-4")
        self.assertTrue(any("model" in m for s, m in check("code-reviewer.md", body, "agents") if s == "ERROR"))

    def test_missing_color(self):
        body = self.GOOD.replace("color: blue\n", "")
        self.assertTrue(any("color" in m for s, m in check("code-reviewer.md", body, "agents") if s == "ERROR"))

    def test_name_differs_from_file_is_a_warning(self):
        findings = check("other.md", self.GOOD, "agents")
        self.assertEqual(severities(findings), {"WARNING"})


if __name__ == "__main__":
    unittest.main()
