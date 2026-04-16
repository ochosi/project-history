#!/usr/bin/env python3
"""Tests for fetch-jira-history script."""

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the module
import importlib.util
spec = importlib.util.spec_from_file_location(
    "fetch_jira",
    Path(__file__).parent.parent / "fetch-jira-history"
)
fetch_jira = importlib.util.module_from_spec(spec)


class TestJiraHistoryFetcher(unittest.TestCase):
    """Test cases for JiraHistoryFetcher class."""

    def setUp(self):
        """Set up test fixtures."""
        spec.loader.exec_module(fetch_jira)
        self.output_dir = Path("/tmp/test-history-jira")
        self.fetcher = fetch_jira.JiraHistoryFetcher(
            jira_url="https://test.atlassian.net",
            project_key="TEST",
            token="fake-token",
            output_dir=str(self.output_dir),
            verbose=False
        )

    def test_sanitize_filename(self):
        """Test filename sanitization."""
        result = self.fetcher.sanitize_filename("TEST-123: Fix/Bug?")
        self.assertNotIn(":", result)
        self.assertNotIn("/", result)
        self.assertNotIn("?", result)

    def test_format_date(self):
        """Test date formatting."""
        result = self.fetcher.format_date("2023-01-15T14:30:00.000+0000")
        self.assertIn("January", result)
        self.assertIn("2023", result)

        result = self.fetcher.format_date(None)
        self.assertEqual(result, "N/A")

    def test_format_description_string(self):
        """Test description formatting for plain strings."""
        result = self.fetcher._format_description("Plain text description")
        self.assertEqual(result, "Plain text description")

    def test_format_description_empty(self):
        """Test description formatting for empty input."""
        result = self.fetcher._format_description("")
        self.assertEqual(result, "*No description provided*")

        result = self.fetcher._format_description(None)
        self.assertEqual(result, "*No description provided*")

    def test_format_description_adf(self):
        """Test Atlassian Document Format conversion."""
        adf = {
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "Test paragraph"}
                    ]
                }
            ]
        }
        result = self.fetcher._format_description(adf)
        self.assertIn("Test paragraph", result)

    def test_extract_text_from_node(self):
        """Test text extraction from ADF nodes."""
        node = {
            "content": [
                {"type": "text", "text": "Plain text"},
                {
                    "type": "text",
                    "text": "Bold text",
                    "marks": [{"type": "strong"}]
                }
            ]
        }
        result = self.fetcher._extract_text_from_node(node)
        self.assertIn("Plain text", result)
        self.assertIn("**Bold text**", result)

    def test_generate_issue_markdown(self):
        """Test Jira issue markdown generation."""
        issue = {
            "key": "TEST-123",
            "fields": {
                "summary": "Test issue",
                "description": "Test description",
                "status": {"name": "Done"},
                "issuetype": {"name": "Bug"},
                "priority": {"name": "High"},
                "created": "2023-01-01T00:00:00.000+0000",
                "updated": "2023-01-02T00:00:00.000+0000",
                "resolutiondate": "2023-01-02T00:00:00.000+0000",
                "reporter": {"displayName": "Reporter"},
                "assignee": {"displayName": "Assignee"},
                "labels": ["backend"],
                "components": [{"name": "API"}]
            }
        }

        markdown = self.fetcher.generate_issue_markdown(issue, [])

        # Check frontmatter
        self.assertIn("type: jira_issue", markdown)
        self.assertIn("key: TEST-123", markdown)
        self.assertIn("status: Done", markdown)

        # Check content
        self.assertIn("# TEST-123", markdown)
        self.assertIn("Test issue", markdown)


if __name__ == "__main__":
    unittest.main()
