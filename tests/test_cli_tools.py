#!/usr/bin/env python3
"""Tests for CLI tool functionality."""

import subprocess
import sys
import unittest
from pathlib import Path


class TestCLITools(unittest.TestCase):
    """Test cases for command-line tools."""

    def setUp(self):
        """Set up test fixtures."""
        self.repo_root = Path(__file__).parent.parent

    def test_fetch_github_help(self):
        """Test fetch-github-history help output."""
        result = subprocess.run(
            [sys.executable, str(self.repo_root / "fetch-github-history"), "--help"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("GitHub", result.stdout)
        self.assertIn("--repo", result.stdout)

    def test_fetch_gitlab_help(self):
        """Test fetch-gitlab-history help output."""
        result = subprocess.run(
            [sys.executable, str(self.repo_root / "fetch-gitlab-history"), "--help"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("GitLab", result.stdout)
        self.assertIn("--project", result.stdout)

    def test_fetch_jira_help(self):
        """Test fetch-jira-history help output."""
        result = subprocess.run(
            [sys.executable, str(self.repo_root / "fetch-jira-history"), "--help"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Jira", result.stdout)
        self.assertIn("--project", result.stdout)

    def test_fetch_history_help(self):
        """Test fetch-history help output."""
        result = subprocess.run(
            [sys.executable, str(self.repo_root / "fetch-history"), "--help"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("platforms", result.stdout.lower())

    def test_generate_history_help(self):
        """Test generate-history-draft help output."""
        result = subprocess.run(
            [sys.executable, str(self.repo_root / "generate-history-draft"), "--help"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("history", result.stdout.lower())

    def test_fetch_github_dry_run(self):
        """Test fetch-github-history dry run."""
        result = subprocess.run(
            [
                sys.executable,
                str(self.repo_root / "fetch-github-history"),
                "--repo", "test/repo",
                "--dry-run"
            ],
            capture_output=True,
            text=True,
            env={"GITHUB_TOKEN": "fake-token"}
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Dry run", result.stdout)

    def test_fetch_gitlab_dry_run(self):
        """Test fetch-gitlab-history dry run."""
        result = subprocess.run(
            [
                sys.executable,
                str(self.repo_root / "fetch-gitlab-history"),
                "--project", "test/repo",
                "--dry-run"
            ],
            capture_output=True,
            text=True,
            env={"GITLAB_TOKEN": "fake-token"}
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Dry run", result.stdout)

    def test_fetch_jira_dry_run(self):
        """Test fetch-jira-history dry run."""
        result = subprocess.run(
            [
                sys.executable,
                str(self.repo_root / "fetch-jira-history"),
                "--project", "TEST",
                "--jira-url", "https://test.atlassian.net",
                "--dry-run"
            ],
            capture_output=True,
            text=True,
            env={"JIRA_TOKEN": "fake-token"}
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Dry run", result.stdout)

    def test_scripts_are_executable(self):
        """Test that all scripts are marked as executable."""
        scripts = [
            "fetch-github-history",
            "fetch-gitlab-history",
            "fetch-jira-history",
            "fetch-history",
            "generate-history-draft",
            "setup-project"
        ]

        for script in scripts:
            script_path = self.repo_root / script
            self.assertTrue(script_path.exists(), f"{script} does not exist")

            # Check if file is executable
            import os
            self.assertTrue(
                os.access(script_path, os.X_OK),
                f"{script} is not executable"
            )

    def test_scripts_have_python_shebang(self):
        """Test that all scripts have proper Python shebang."""
        scripts = [
            "fetch-github-history",
            "fetch-gitlab-history",
            "fetch-jira-history",
            "fetch-history",
            "generate-history-draft",
            "setup-project"
        ]

        for script in scripts:
            script_path = self.repo_root / script
            with open(script_path, 'r') as f:
                first_line = f.readline().strip()

            self.assertTrue(
                first_line.startswith("#!/usr/bin/env python"),
                f"{script} has invalid shebang: {first_line}"
            )


if __name__ == "__main__":
    unittest.main()
