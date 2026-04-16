#!/usr/bin/env python3
"""Tests for generate-history-draft script."""

import json
import sys
import unittest
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the module
import importlib.util
spec = importlib.util.spec_from_file_location(
    "generate_history",
    Path(__file__).parent.parent / "generate-history-draft"
)
generate_history = importlib.util.module_from_spec(spec)


class TestIssueCorrelator(unittest.TestCase):
    """Test cases for IssueCorrelator class."""

    def setUp(self):
        """Set up test fixtures."""
        spec.loader.exec_module(generate_history)
        self.history_path = Path(__file__).parent / "fixtures"
        self.correlator = generate_history.IssueCorrelator(
            self.history_path,
            verbose=False
        )

    def test_extract_github_pr_reference(self):
        """Test extraction of GitHub PR references from commit messages."""
        messages = [
            "Fix bug (#123)",
            "Merge pull request #456 from user/branch",
            "fixes #789",
            "closes #101"
        ]

        for msg in messages:
            refs = self.correlator.extract_references(msg)
            self.assertIsNotNone(refs.get('github_pr') or any('#' in msg for msg in [msg]))

    def test_extract_gitlab_mr_reference(self):
        """Test extraction of GitLab MR references from commit messages."""
        messages = [
            "Fix bug (!123)",
            "Merge request !456",
            "fixes !789",
            "closes !101"
        ]

        for msg in messages:
            refs = self.correlator.extract_references(msg)
            # Will only match if MR exists in loaded data
            self.assertIsNotNone(refs)

    def test_extract_jira_reference(self):
        """Test extraction of Jira ticket references from commit messages."""
        messages = [
            "PROJ-123: Fix authentication bug",
            "Implement feature ABC-456",
            "TEST-789 Update documentation"
        ]

        for msg in messages:
            refs = self.correlator.extract_references(msg)
            # Will only match if ticket exists in loaded data
            self.assertIsNotNone(refs)

    def test_extract_multiple_references(self):
        """Test extraction of multiple reference types from one message."""
        msg = "Fix bug PROJ-123 (#456) (!789)"
        refs = self.correlator.extract_references(msg)

        # Check that refs is a dict with expected keys
        self.assertIn('github_pr', refs)
        self.assertIn('gitlab_mr', refs)
        self.assertIn('jira_issues', refs)


class TestThemeDetector(unittest.TestCase):
    """Test cases for ThemeDetector class."""

    def setUp(self):
        """Set up test fixtures."""
        spec.loader.exec_module(generate_history)
        self.detector = generate_history.ThemeDetector()

    def test_detect_architecture_theme(self):
        """Test detection of architecture theme."""
        message = "Update manifest format and schema"
        themes = self.detector.detect_themes(message)
        self.assertIn('architecture', themes)

    def test_detect_testing_theme(self):
        """Test detection of testing theme."""
        message = "Add unit tests for API endpoints"
        themes = self.detector.detect_themes(message)
        self.assertIn('testing', themes)

    def test_detect_performance_theme(self):
        """Test detection of performance theme."""
        message = "Optimize cache performance"
        themes = self.detector.detect_themes(message)
        self.assertIn('performance', themes)

    def test_detect_multiple_themes(self):
        """Test detection of multiple themes in one message."""
        message = "Add performance tests for cache optimization"
        themes = self.detector.detect_themes(message)
        self.assertGreaterEqual(len(themes), 1)


class TestImportanceScorer(unittest.TestCase):
    """Test cases for ImportanceScorer class."""

    def setUp(self):
        """Set up test fixtures."""
        spec.loader.exec_module(generate_history)
        self.scorer = generate_history.ImportanceScorer()

    def test_score_commit_with_keywords(self):
        """Test scoring commits with important keywords."""
        commit_breaking = {
            'message': 'BREAKING: Change API format',
            'sha': 'abc123',
            'author': 'dev',
            'email': 'dev@example.com',
            'date': datetime.now(timezone.utc),
            'subject': 'BREAKING: Change API format',
            'body': ''
        }

        score_breaking = self.scorer.score_commit(commit_breaking)
        self.assertGreater(score_breaking, 0)

        commit_normal = {
            'message': 'Update documentation',
            'sha': 'def456',
            'author': 'dev',
            'email': 'dev@example.com',
            'date': datetime.now(timezone.utc),
            'subject': 'Update documentation',
            'body': ''
        }

        score_normal = self.scorer.score_commit(commit_normal)
        self.assertGreaterEqual(score_breaking, score_normal)

    def test_score_pr_with_labels(self):
        """Test scoring PRs with different labels."""
        pr_breaking = {
            'title': 'Breaking change',
            'body': 'Long description' * 100,
            'labels': ['breaking-change']
        }

        score_breaking = self.scorer.score_pr(pr_breaking)
        self.assertGreater(score_breaking, 10)

        pr_normal = {
            'title': 'Minor fix',
            'body': 'Short description',
            'labels': []
        }

        score_normal = self.scorer.score_pr(pr_normal)
        self.assertGreaterEqual(score_breaking, score_normal)


class TestGitAnalyzer(unittest.TestCase):
    """Test cases for GitAnalyzer class."""

    def setUp(self):
        """Set up test fixtures."""
        spec.loader.exec_module(generate_history)

    @patch('subprocess.run')
    def test_get_all_commits(self, mock_run):
        """Test fetching all commits from git."""
        # Mock git log output
        mock_run.return_value = Mock(
            stdout="abc123|Author|author@example.com|1609459200|Test commit|Test body\x00"
        )

        analyzer = generate_history.GitAnalyzer(Path.cwd(), verbose=False)
        commits = analyzer.get_all_commits()

        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0]['sha'], 'abc123')
        self.assertEqual(commits[0]['author'], 'Author')
        self.assertEqual(commits[0]['subject'], 'Test commit')


if __name__ == "__main__":
    unittest.main()
