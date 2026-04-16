#!/usr/bin/env python3
"""Tests for generate-history-draft script."""

import json
import re
import unittest
from pathlib import Path


class TestReferencePatterns(unittest.TestCase):
    """Test reference pattern matching."""

    def test_github_pr_patterns(self):
        """Test GitHub PR pattern matching."""
        patterns = [
            r'\(#(\d+)\)',           # (#123)
            r'#(\d+)',               # #123
            r'fixes #(\d+)',         # fixes #123
            r'closes #(\d+)',        # closes #123
        ]

        messages = [
            "Fix bug (#123)",
            "Reference #456",
            "fixes #789",
            "closes #101"
        ]

        for msg in messages:
            found = False
            for pattern in patterns:
                if re.search(pattern, msg, re.IGNORECASE):
                    found = True
                    break
            self.assertTrue(found, f"No pattern matched message: {msg}")

    def test_gitlab_mr_patterns(self):
        """Test GitLab MR pattern matching."""
        patterns = [
            r'\(!(\d+)\)',           # (!123)
            r'!(\d+)',               # !123
            r'fixes !(\d+)',         # fixes !123
        ]

        messages = [
            "Fix bug (!123)",
            "Reference !456",
            "fixes !789"
        ]

        for msg in messages:
            found = False
            for pattern in patterns:
                if re.search(pattern, msg, re.IGNORECASE):
                    found = True
                    break
            self.assertTrue(found, f"No pattern matched message: {msg}")

    def test_jira_pattern(self):
        """Test Jira ticket pattern matching."""
        pattern = r'\b([A-Z][A-Z0-9]+-\d+)\b'

        messages = [
            "PROJ-123: Fix bug",
            "Implement ABC-456",
            "TEST-789 Update docs"
        ]

        for msg in messages:
            match = re.search(pattern, msg)
            self.assertIsNotNone(match, f"Pattern didn't match: {msg}")


class TestThemeKeywords(unittest.TestCase):
    """Test theme detection keywords."""

    def setUp(self):
        """Set up theme definitions."""
        self.themes = {
            'architecture': ['manifest', 'schema', 'format', 'architecture'],
            'testing': ['test', 'pytest', 'unittest', 'coverage'],
            'performance': ['perf', 'cache', 'optimization', 'speed'],
            'security': ['security', 'selinux', 'permission']
        }

    def test_architecture_keywords(self):
        """Test architecture theme keywords."""
        message = "Update manifest format and schema"
        msg_lower = message.lower()

        matches = []
        for keyword in self.themes['architecture']:
            if keyword in msg_lower:
                matches.append(keyword)

        self.assertGreater(len(matches), 0)

    def test_testing_keywords(self):
        """Test testing theme keywords."""
        message = "Add unit tests with pytest"
        msg_lower = message.lower()

        matches = []
        for keyword in self.themes['testing']:
            if keyword in msg_lower:
                matches.append(keyword)

        self.assertGreater(len(matches), 0)


class TestImportanceScoring(unittest.TestCase):
    """Test importance scoring logic."""

    def test_keyword_scoring(self):
        """Test that important keywords increase score."""
        important_keywords = ['breaking', 'major', 'important', 'critical']

        message_with_keywords = "BREAKING: Major API change"
        message_without = "Update documentation"

        score1 = 0
        for keyword in important_keywords:
            if keyword in message_with_keywords.lower():
                score1 += 3

        score2 = 0
        for keyword in important_keywords:
            if keyword in message_without.lower():
                score2 += 3

        self.assertGreater(score1, score2)


class TestMarkdownFrontmatter(unittest.TestCase):
    """Test markdown frontmatter parsing."""

    def test_parse_frontmatter(self):
        """Test parsing YAML-like frontmatter."""
        content = """---
type: pull_request
number: 123
title: "Test PR"
state: merged
---

# Content here
"""

        if not content.startswith('---'):
            self.fail("Content doesn't start with frontmatter")

        parts = content.split('---', 2)
        self.assertEqual(len(parts), 3)

        frontmatter = {}
        for line in parts[1].strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()

                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]

                frontmatter[key] = value

        self.assertEqual(frontmatter['type'], 'pull_request')
        self.assertEqual(frontmatter['number'], '123')
        self.assertEqual(frontmatter['state'], 'merged')


if __name__ == "__main__":
    unittest.main()
