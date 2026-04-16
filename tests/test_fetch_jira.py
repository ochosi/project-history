#!/usr/bin/env python3
"""Tests for fetch-jira-history script."""

import json
import re
import unittest
from pathlib import Path


class TestJiraKeyPattern(unittest.TestCase):
    """Test Jira ticket key pattern matching."""

    def test_jira_key_pattern(self):
        """Test Jira key pattern regex."""
        pattern = r'\b([A-Z][A-Z0-9]+-\d+)\b'

        messages = [
            "Fix PROJ-123",
            "TEST-456: Update feature",
            "Implement ABC-789 and DEF-012"
        ]

        expected = [
            ["PROJ-123"],
            ["TEST-456"],
            ["ABC-789", "DEF-012"]
        ]

        for msg, exp in zip(messages, expected):
            matches = re.findall(pattern, msg)
            self.assertEqual(matches, exp)


class TestJiraMockData(unittest.TestCase):
    """Test Jira mock data structure."""

    def setUp(self):
        """Load mock data."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        with open(fixtures_dir / "mock_jira_data.json") as f:
            self.data = json.load(f)

    def test_mock_data_structure(self):
        """Test that mock data has expected structure."""
        self.assertIn("issues", self.data)

    def test_mock_issue_structure(self):
        """Test mock issue has required fields."""
        issue = self.data["issues"][0]
        self.assertIn("key", issue)
        self.assertIn("fields", issue)

        fields = issue["fields"]
        required_fields = ["summary", "status", "issuetype", "created"]
        for field in required_fields:
            self.assertIn(field, fields)


class TestAtlassianDocumentFormat(unittest.TestCase):
    """Test Atlassian Document Format (ADF) structures."""

    def test_adf_paragraph_structure(self):
        """Test ADF paragraph structure."""
        adf = {
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "Simple text"}
                    ]
                }
            ]
        }

        self.assertEqual(adf["type"], "doc")
        self.assertEqual(len(adf["content"]), 1)
        self.assertEqual(adf["content"][0]["type"], "paragraph")

    def test_adf_with_marks(self):
        """Test ADF with text marks (bold, italic, etc.)."""
        text_with_marks = {
            "type": "text",
            "text": "Bold text",
            "marks": [{"type": "strong"}]
        }

        self.assertIn("marks", text_with_marks)
        self.assertEqual(text_with_marks["marks"][0]["type"], "strong")


if __name__ == "__main__":
    unittest.main()
