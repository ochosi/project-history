#!/usr/bin/env python3
"""Tests for fetch-github-history script."""

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import after path modification
import importlib.util
spec = importlib.util.spec_from_file_location(
    "fetch_github",
    Path(__file__).parent.parent / "fetch-github-history"
)
fetch_github = importlib.util.module_from_spec(spec)


class TestGitHubHistoryFetcher(unittest.TestCase):
    """Test cases for GitHubHistoryFetcher class."""

    def setUp(self):
        """Set up test fixtures."""
        spec.loader.exec_module(fetch_github)
        self.output_dir = Path("/tmp/test-history")
        self.fetcher = fetch_github.GitHubHistoryFetcher(
            owner="test-owner",
            repo="test-repo",
            token="fake-token",
            output_dir=str(self.output_dir),
            verbose=False
        )

    def test_sanitize_filename(self):
        """Test filename sanitization."""
        # Test basic sanitization
        result = self.fetcher.sanitize_filename("Test: File/Name?")
        self.assertNotIn(":", result)
        self.assertNotIn("/", result)
        self.assertNotIn("?", result)

        # Test length limit
        long_name = "a" * 100
        result = self.fetcher.sanitize_filename(long_name, max_length=50)
        self.assertLessEqual(len(result), 50)

        # Test empty string
        result = self.fetcher.sanitize_filename("")
        self.assertEqual(result, "untitled")

    def test_format_date(self):
        """Test date formatting."""
        # Test valid ISO date
        result = self.fetcher.format_date("2023-01-15T14:30:00Z")
        self.assertIn("January", result)
        self.assertIn("2023", result)

        # Test None
        result = self.fetcher.format_date(None)
        self.assertEqual(result, "N/A")

        # Test empty string
        result = self.fetcher.format_date("")
        self.assertEqual(result, "N/A")

    def test_generate_issue_markdown(self):
        """Test issue markdown generation."""
        issue = {
            "number": 123,
            "title": "Test Issue",
            "state": "CLOSED",
            "createdAt": "2023-01-01T00:00:00Z",
            "updatedAt": "2023-01-02T00:00:00Z",
            "closedAt": "2023-01-02T00:00:00Z",
            "author": {"login": "testuser"},
            "labels": {"nodes": [{"name": "bug"}]},
            "body": "Test body",
            "comments": {"nodes": []}
        }

        markdown = self.fetcher.generate_issue_markdown(issue)

        # Check frontmatter
        self.assertIn("type: issue", markdown)
        self.assertIn("number: 123", markdown)
        self.assertIn("state: closed", markdown)

        # Check content
        self.assertIn("# Issue #123", markdown)
        self.assertIn("Test Issue", markdown)
        self.assertIn("Test body", markdown)

    def test_generate_pr_markdown(self):
        """Test PR markdown generation."""
        pr = {
            "number": 456,
            "title": "Test PR",
            "state": "MERGED",
            "merged": True,
            "createdAt": "2023-01-01T00:00:00Z",
            "updatedAt": "2023-01-02T00:00:00Z",
            "mergedAt": "2023-01-02T00:00:00Z",
            "author": {"login": "contributor"},
            "baseRefName": "main",
            "headRefName": "feature",
            "labels": {"nodes": []},
            "body": "Test PR body",
            "comments": {"nodes": []},
            "reviews": {"nodes": []}
        }

        markdown = self.fetcher.generate_pr_markdown(pr)

        # Check frontmatter
        self.assertIn("type: pull_request", markdown)
        self.assertIn("number: 456", markdown)
        self.assertIn("state: merged", markdown)

        # Check content
        self.assertIn("# Pull Request #456", markdown)
        self.assertIn("Test PR", markdown)


class TestGitRemoteParsing(unittest.TestCase):
    """Test cases for git remote URL parsing."""

    def setUp(self):
        """Set up test fixtures."""
        spec.loader.exec_module(fetch_github)

    def test_parse_github_ssh_url(self):
        """Test parsing GitHub SSH URLs."""
        url = "git@github.com:owner/repo.git"
        owner, repo = fetch_github.parse_git_remote(url)
        self.assertEqual(owner, "owner")
        self.assertEqual(repo, "repo")

    def test_parse_github_https_url(self):
        """Test parsing GitHub HTTPS URLs."""
        url = "https://github.com/owner/repo.git"
        owner, repo = fetch_github.parse_git_remote(url)
        self.assertEqual(owner, "owner")
        self.assertEqual(repo, "repo")

    def test_parse_github_https_url_without_git(self):
        """Test parsing GitHub HTTPS URLs without .git suffix."""
        url = "https://github.com/owner/repo"
        owner, repo = fetch_github.parse_git_remote(url)
        self.assertEqual(owner, "owner")
        self.assertEqual(repo, "repo")


if __name__ == "__main__":
    unittest.main()
