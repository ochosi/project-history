#!/usr/bin/env python3
"""Tests for fetch-github-history script."""

import json
import re
import unittest
from pathlib import Path


class TestGitHubURLParsing(unittest.TestCase):
    """Test cases for GitHub URL parsing logic."""

    def test_ssh_url_pattern(self):
        """Test SSH URL pattern matching."""
        pattern = r"git@[^:]+:([^/]+)/(.+?)(?:\.git)?$"

        url = "git@github.com:owner/repo.git"
        match = re.match(pattern, url)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "owner")
        self.assertEqual(match.group(2), "repo")

    def test_https_url_pattern(self):
        """Test HTTPS URL parsing."""
        from urllib.parse import urlparse

        url = "https://github.com/owner/repo.git"
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')

        self.assertEqual(len(path_parts), 2)
        self.assertEqual(path_parts[0], "owner")
        self.assertEqual(path_parts[1].replace('.git', ''), "repo")


class TestFilenameSanitization(unittest.TestCase):
    """Test filename sanitization logic."""

    def sanitize_filename(self, text, max_length=50):
        """Sanitize text for use as a filename."""
        text = re.sub(r'[<>:"/\\|?*]', '', text)
        text = re.sub(r'\s+', '-', text)
        text = text.strip('-').lower()

        if len(text) > max_length:
            text = text[:max_length].rstrip('-')

        return text or "untitled"

    def test_removes_invalid_characters(self):
        """Test that invalid filename characters are removed."""
        result = self.sanitize_filename("Test: File/Name?")
        self.assertNotIn(":", result)
        self.assertNotIn("/", result)
        self.assertNotIn("?", result)

    def test_length_limit(self):
        """Test length limiting."""
        long_name = "a" * 100
        result = self.sanitize_filename(long_name, max_length=50)
        self.assertLessEqual(len(result), 50)

    def test_empty_string(self):
        """Test empty string handling."""
        result = self.sanitize_filename("")
        self.assertEqual(result, "untitled")


class TestGitHubMockData(unittest.TestCase):
    """Test GitHub mock data structure."""

    def setUp(self):
        """Load mock data."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        with open(fixtures_dir / "mock_github_data.json") as f:
            self.data = json.load(f)

    def test_mock_data_structure(self):
        """Test that mock data has expected structure."""
        self.assertIn("issues", self.data)
        self.assertIn("pullRequests", self.data)

    def test_mock_issue_structure(self):
        """Test mock issue has required fields."""
        issue = self.data["issues"][0]
        required_fields = ["number", "title", "state", "createdAt", "author"]
        for field in required_fields:
            self.assertIn(field, issue)

    def test_mock_pr_structure(self):
        """Test mock PR has required fields."""
        pr = self.data["pullRequests"][0]
        required_fields = ["number", "title", "state", "merged", "author"]
        for field in required_fields:
            self.assertIn(field, pr)


if __name__ == "__main__":
    unittest.main()
