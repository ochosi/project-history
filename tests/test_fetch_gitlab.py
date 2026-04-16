#!/usr/bin/env python3
"""Tests for fetch-gitlab-history script."""

import json
import re
import unittest
from pathlib import Path
from urllib.parse import urlparse


class TestGitLabURLParsing(unittest.TestCase):
    """Test cases for GitLab URL parsing logic."""

    def test_ssh_url_pattern(self):
        """Test SSH URL pattern matching."""
        pattern = r"git@([^:]+):(.+?)(?:\.git)?$"

        url = "git@gitlab.com:namespace/project.git"
        match = re.match(pattern, url)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "gitlab.com")
        self.assertEqual(match.group(2), "namespace/project")

    def test_https_url_parsing(self):
        """Test HTTPS URL parsing."""
        url = "https://gitlab.com/namespace/project.git"
        parsed = urlparse(url)

        gitlab_url = f"{parsed.scheme}://{parsed.netloc}"
        project_path = parsed.path.strip('/').replace('.git', '')

        self.assertEqual(gitlab_url, "https://gitlab.com")
        self.assertEqual(project_path, "namespace/project")

    def test_self_hosted_gitlab(self):
        """Test parsing self-hosted GitLab URLs."""
        url = "https://gitlab.example.com/team/repo.git"
        parsed = urlparse(url)

        gitlab_url = f"{parsed.scheme}://{parsed.netloc}"
        project_path = parsed.path.strip('/').replace('.git', '')

        self.assertEqual(gitlab_url, "https://gitlab.example.com")
        self.assertEqual(project_path, "team/repo")


class TestGitLabMockData(unittest.TestCase):
    """Test GitLab mock data structure."""

    def setUp(self):
        """Load mock data."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        with open(fixtures_dir / "mock_gitlab_data.json") as f:
            self.data = json.load(f)

    def test_mock_data_structure(self):
        """Test that mock data has expected structure."""
        self.assertIn("issues", self.data)
        self.assertIn("merge_requests", self.data)

    def test_mock_issue_structure(self):
        """Test mock issue has required fields."""
        issue = self.data["issues"][0]
        required_fields = ["iid", "title", "state", "created_at", "author"]
        for field in required_fields:
            self.assertIn(field, issue)

    def test_mock_mr_structure(self):
        """Test mock MR has required fields."""
        mr = self.data["merge_requests"][0]
        required_fields = ["iid", "title", "state", "author", "target_branch"]
        for field in required_fields:
            self.assertIn(field, mr)


if __name__ == "__main__":
    unittest.main()
