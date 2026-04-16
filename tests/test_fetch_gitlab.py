#!/usr/bin/env python3
"""Tests for fetch-gitlab-history script."""

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the module
import importlib.util
spec = importlib.util.spec_from_file_location(
    "fetch_gitlab",
    Path(__file__).parent.parent / "fetch-gitlab-history"
)
fetch_gitlab = importlib.util.module_from_spec(spec)


class TestGitLabHistoryFetcher(unittest.TestCase):
    """Test cases for GitLabHistoryFetcher class."""

    def setUp(self):
        """Set up test fixtures."""
        spec.loader.exec_module(fetch_gitlab)
        self.output_dir = Path("/tmp/test-history-gitlab")
        self.fetcher = fetch_gitlab.GitLabHistoryFetcher(
            project_id="test/project",
            token="fake-token",
            gitlab_url="https://gitlab.com",
            output_dir=str(self.output_dir),
            verbose=False
        )

    def test_sanitize_filename(self):
        """Test filename sanitization."""
        result = self.fetcher.sanitize_filename("Test: MR/Name?")
        self.assertNotIn(":", result)
        self.assertNotIn("/", result)
        self.assertNotIn("?", result)

    def test_format_date(self):
        """Test date formatting."""
        result = self.fetcher.format_date("2023-01-15T14:30:00Z")
        self.assertIn("January", result)
        self.assertIn("2023", result)

        result = self.fetcher.format_date(None)
        self.assertEqual(result, "N/A")

    def test_generate_issue_markdown(self):
        """Test issue markdown generation."""
        issue = {
            "iid": 123,
            "title": "Test Issue",
            "state": "closed",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-02T00:00:00Z",
            "closed_at": "2023-01-02T00:00:00Z",
            "author": {"username": "testuser"},
            "labels": ["bug"],
            "description": "Test description",
            "web_url": "https://gitlab.com/test/project/-/issues/123"
        }

        markdown = self.fetcher.generate_issue_markdown(issue, [])

        # Check frontmatter
        self.assertIn("type: issue", markdown)
        self.assertIn("number: 123", markdown)
        self.assertIn("state: closed", markdown)

        # Check content
        self.assertIn("# Issue #123", markdown)
        self.assertIn("Test Issue", markdown)

    def test_generate_mr_markdown(self):
        """Test MR markdown generation."""
        mr = {
            "iid": 456,
            "title": "Test MR",
            "state": "merged",
            "merged_at": "2023-01-02T00:00:00Z",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-02T00:00:00Z",
            "author": {"username": "contributor"},
            "target_branch": "main",
            "source_branch": "feature",
            "labels": [],
            "description": "Test MR description",
            "web_url": "https://gitlab.com/test/project/-/merge_requests/456"
        }

        markdown = self.fetcher.generate_mr_markdown(mr, [])

        # Check frontmatter
        self.assertIn("type: merge_request", markdown)
        self.assertIn("number: 456", markdown)
        self.assertIn("state: merged", markdown)

        # Check content
        self.assertIn("# Merge Request !456", markdown)
        self.assertIn("Test MR", markdown)


class TestGitLabRemoteParsing(unittest.TestCase):
    """Test cases for GitLab git remote URL parsing."""

    def setUp(self):
        """Set up test fixtures."""
        spec.loader.exec_module(fetch_gitlab)

    def test_parse_gitlab_ssh_url(self):
        """Test parsing GitLab SSH URLs."""
        url = "git@gitlab.com:namespace/project.git"
        gitlab_url, project_path = fetch_gitlab.parse_git_remote(url)
        self.assertEqual(gitlab_url, "https://gitlab.com")
        self.assertEqual(project_path, "namespace/project")

    def test_parse_gitlab_https_url(self):
        """Test parsing GitLab HTTPS URLs."""
        url = "https://gitlab.com/namespace/project.git"
        gitlab_url, project_path = fetch_gitlab.parse_git_remote(url)
        self.assertEqual(gitlab_url, "https://gitlab.com")
        self.assertEqual(project_path, "namespace/project")

    def test_parse_self_hosted_gitlab(self):
        """Test parsing self-hosted GitLab URLs."""
        url = "https://gitlab.example.com/team/repo.git"
        gitlab_url, project_path = fetch_gitlab.parse_git_remote(url)
        self.assertEqual(gitlab_url, "https://gitlab.example.com")
        self.assertEqual(project_path, "team/repo")


if __name__ == "__main__":
    unittest.main()
