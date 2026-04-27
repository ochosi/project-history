#!/usr/bin/env python3
"""Tests for generate-history-draft script."""

import importlib.util
from importlib.machinery import SourceFileLoader
from datetime import datetime, timezone
import json
import re
import tempfile
import unittest
from pathlib import Path

# Import ThemeDetector from generate-history-draft script
_script_path = str(Path(__file__).parent.parent / "generate-history-draft")
_loader = SourceFileLoader("generate_history_draft", _script_path)
_spec = importlib.util.spec_from_loader("generate_history_draft", _loader)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

ThemeDetector = _mod.ThemeDetector
ImportanceScorer = _mod.ImportanceScorer
HistoryGenerator = _mod.HistoryGenerator
# load_analysis_config will be imported after implementation


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


class TestConfigurableThemeDetector(unittest.TestCase):
    """Test ThemeDetector with configurable themes."""

    def test_custom_themes_used_when_provided(self):
        """Test that custom themes are used when provided."""
        custom_themes = {
            'databases': {
                'keywords': ['mysql', 'postgres', 'mongodb', 'database'],
                'description': 'Database-related changes'
            },
            'frontend': {
                'keywords': ['react', 'vue', 'angular', 'ui', 'css'],
                'description': 'Frontend changes'
            }
        }

        detector = ThemeDetector(themes=custom_themes)

        # Should match custom themes
        themes = detector.detect_themes("Add mysql database support")
        self.assertIn('databases', themes)

        themes = detector.detect_themes("Update react ui components")
        self.assertIn('frontend', themes)

    def test_custom_themes_no_false_positives(self):
        """Test that old osbuild keywords don't match when custom themes are used."""
        custom_themes = {
            'databases': {
                'keywords': ['mysql', 'postgres', 'mongodb'],
                'description': 'Database-related changes'
            }
        }

        detector = ThemeDetector(themes=custom_themes)

        # Should NOT match osbuild-specific keywords like 'pipeline'
        themes = detector.detect_themes("Update pipeline architecture")
        self.assertEqual(len(themes), 0)

        # Should NOT match osbuild stages
        themes = detector.detect_themes("Add new org.osbuild.rpm stage")
        self.assertEqual(len(themes), 0)

    def test_default_themes_when_none_provided(self):
        """Test that default themes work when no custom themes provided."""
        detector = ThemeDetector()

        # Should still detect some themes with generic keywords
        themes = detector.detect_themes("Add unit tests for API")
        self.assertGreater(len(themes), 0)

    def test_default_themes_are_generic(self):
        """Test that default themes don't include osbuild-specific names."""
        detector = ThemeDetector()

        # Get the default themes
        default_themes = detector.themes

        # Should NOT have osbuild-specific theme names
        osbuild_specific = ['stages', 'assemblers', 'sources', 'dnf', 'isolation']
        for theme_name in osbuild_specific:
            self.assertNotIn(theme_name, default_themes,
                           f"Default themes should not include osbuild-specific theme '{theme_name}'")


class TestConfigurableImportanceScorer(unittest.TestCase):
    """Test ImportanceScorer with configurable keywords."""

    def test_custom_arch_keywords(self):
        """Test that custom architectural keywords increase commit score."""
        scorer = ImportanceScorer(
            architectural_keywords=['lmdb', 'openssl', 'rust']
        )

        commit = {
            'message': 'Migrate to lmdb backend for improved performance',
            'hash': 'abc123',
            'author': 'Test Author',
            'date': '2024-01-01'
        }

        score = scorer.score_commit(commit)
        # Should get architectural keyword bonus (>= 5 points)
        self.assertGreaterEqual(score, 5)

    def test_default_arch_keywords_are_generic(self):
        """Test that default architectural keywords don't include project-specific terms."""
        scorer = ImportanceScorer()

        # 'manifest' is osbuild-specific, should NOT get arch bonus
        commit_specific = {
            'message': 'Update manifest format',
            'hash': 'abc123',
            'author': 'Test',
            'date': '2024-01-01'
        }
        score_specific = scorer.score_commit(commit_specific)

        # 'architecture' is generic, should get arch bonus
        commit_generic = {
            'message': 'Redesign core architecture',
            'hash': 'def456',
            'author': 'Test',
            'date': '2024-01-01'
        }
        score_generic = scorer.score_commit(commit_generic)

        # Generic architectural term should score higher
        self.assertGreater(score_generic, score_specific)

    def test_custom_title_keywords_in_pr_scoring(self):
        """Test that custom title keywords increase PR score."""
        scorer = ImportanceScorer(
            title_keywords=['lmdb', 'replication', 'migration']
        )

        pr_data = {
            'title': 'LMDB backend migration',
            'body': 'Migrate the storage layer to LMDB',
            'labels': [],
            'number': 123
        }

        score = scorer.score_pr(pr_data)
        # Should get title keyword bonus (>= 10 points)
        self.assertGreaterEqual(score, 10)

    def test_default_title_keywords_are_generic(self):
        """Test that default title keywords don't include project-specific terms."""
        scorer = ImportanceScorer()

        # 'format' and 'schema' are osbuild-specific
        pr_specific = {
            'title': 'Update manifest format and schema',
            'body': 'Updates to the format',
            'labels': []
        }
        score_specific = scorer.score_pr(pr_specific)

        # 'breaking' and 'migration' are generic
        pr_generic = {
            'title': 'Breaking change: API migration',
            'body': 'Major API migration',
            'labels': []
        }
        score_generic = scorer.score_pr(pr_generic)

        # Generic terms should score higher
        self.assertGreater(score_generic, score_specific)


class TestConfigurablePeriods(unittest.TestCase):
    """Test HistoryGenerator with configurable periods."""

    def test_custom_periods_used(self):
        """Test that custom periods are used when provided."""
        custom_periods = {
            'phase-alpha': {
                'start': '2020-01-01',
                'end': '2021-12-31',
                'description': 'Alpha phase'
            },
            'phase-beta': {
                'start': '2022-01-01',
                'end': '2023-12-31',
                'description': 'Beta phase'
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir) / "repo"
            history_path = Path(tmpdir) / "history"
            output_path = Path(tmpdir) / "output"

            repo_path.mkdir()
            history_path.mkdir()
            output_path.mkdir()

            gen = HistoryGenerator(
                repo_path=repo_path,
                history_path=history_path,
                output_path=output_path,
                periods=custom_periods
            )

            # Should use custom periods
            self.assertEqual(gen.periods, custom_periods)
            self.assertIn('phase-alpha', gen.periods)
            self.assertIn('phase-beta', gen.periods)

    def test_no_osbuild_periods_in_defaults(self):
        """Test that default periods don't include osbuild-specific names."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir) / "repo"
            history_path = Path(tmpdir) / "history"
            output_path = Path(tmpdir) / "output"

            repo_path.mkdir()
            history_path.mkdir()
            output_path.mkdir()

            gen = HistoryGenerator(
                repo_path=repo_path,
                history_path=history_path,
                output_path=output_path
            )

            # Should NOT have osbuild-specific period names
            osbuild_specific_periods = ['genesis', 'foundation', 'maturation', 'production-scale', 'modern-features']
            for period_name in osbuild_specific_periods:
                self.assertNotIn(period_name, gen.periods,
                               f"Default periods should not include osbuild-specific period '{period_name}'")


class TestLoadAnalysisConfig(unittest.TestCase):
    """Test analysis config file loading."""

    def setUp(self):
        self.load_analysis_config = _mod.load_analysis_config

    def test_loads_valid_config(self):
        """Loads and returns a valid config file."""
        config = {
            "themes": {
                "database": {
                    "keywords": ["lmdb", "bdb"],
                    "description": "Database backend"
                }
            },
            "periods": {
                "early": {
                    "start": "2005-01-01",
                    "end": "2010-12-31",
                    "description": "Early development"
                }
            },
            "importance": {
                "architectural_keywords": ["lmdb", "openssl"],
                "title_keywords": ["migration", "breaking"]
            }
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / ".history-analysis-config.json"
            with open(config_path, 'w') as f:
                json.dump(config, f)

            result = self.load_analysis_config(Path(tmpdir))
            self.assertIsNotNone(result)
            self.assertIn('database', result['themes'])
            self.assertIn('early', result['periods'])
            self.assertEqual(result['importance']['architectural_keywords'], ['lmdb', 'openssl'])

    def test_returns_none_when_missing(self):
        """Returns None when no config file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.load_analysis_config(Path(tmpdir))
            self.assertIsNone(result)

    def test_partial_config_fills_defaults(self):
        """Config with only themes still works (periods/importance get None)."""
        config = {
            "themes": {
                "testing": {
                    "keywords": ["test"],
                    "description": "Tests"
                }
            }
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / ".history-analysis-config.json"
            with open(config_path, 'w') as f:
                json.dump(config, f)

            result = self.load_analysis_config(Path(tmpdir))
            self.assertIsNotNone(result)
            self.assertIn('testing', result['themes'])
            self.assertIsNone(result.get('periods'))


class TestThemeDiscovery(unittest.TestCase):
    """Test automatic theme discovery from commit messages."""

    def setUp(self):
        self.DiscoveryAnalyzer = _mod.DiscoveryAnalyzer

    def test_discovers_themes_from_keywords(self):
        """Discovers themes from frequently occurring terms in commits."""
        commits = [
            {'message': 'Fix replication changelog sync', 'date': None},
            {'message': 'Update replication protocol', 'date': None},
            {'message': 'Fix replica agreement', 'date': None},
            {'message': 'Add test for auth module', 'date': None},
            {'message': 'Add test for login flow', 'date': None},
            {'message': 'Fix test runner config', 'date': None},
            {'message': 'Improve cache performance', 'date': None},
            {'message': 'Optimize query performance', 'date': None},
        ]
        analyzer = self.DiscoveryAnalyzer(commits)
        themes = analyzer.discover_themes()
        self.assertGreater(len(themes), 0)
        all_keywords = []
        for theme_data in themes.values():
            all_keywords.extend(theme_data['keywords'])
        self.assertTrue(
            any('replicat' in kw for kw in all_keywords) or
            any('test' in kw for kw in all_keywords),
            f"Expected replication or test keywords, got: {all_keywords}"
        )

    def test_filters_noise_words(self):
        """Common git verbs should not appear as theme keywords."""
        commits = [
            {'message': 'fix bug in module', 'date': None},
            {'message': 'add new feature', 'date': None},
            {'message': 'update dependency', 'date': None},
            {'message': 'remove old code', 'date': None},
            {'message': 'merge branch main', 'date': None},
        ]
        analyzer = self.DiscoveryAnalyzer(commits)
        themes = analyzer.discover_themes()
        all_keywords = []
        for theme_data in themes.values():
            all_keywords.extend(theme_data['keywords'])
        noise = {'fix', 'add', 'update', 'remove', 'merge', 'bug', 'new', 'old', 'branch', 'main'}
        found_noise = set(all_keywords) & noise
        self.assertEqual(found_noise, set(),
                         f"Noise words found in themes: {found_noise}")

    def test_returns_dict_with_correct_structure(self):
        """Each theme has keywords list and description string."""
        commits = [
            {'message': 'replication sync fix', 'date': None},
            {'message': 'replication changelog', 'date': None},
            {'message': 'replication test', 'date': None},
        ]
        analyzer = self.DiscoveryAnalyzer(commits)
        themes = analyzer.discover_themes()
        for name, data in themes.items():
            self.assertIsInstance(name, str)
            self.assertIn('keywords', data)
            self.assertIn('description', data)
            self.assertIsInstance(data['keywords'], list)
            self.assertIsInstance(data['description'], str)
            self.assertGreater(len(data['keywords']), 0)


class TestPeriodDiscovery(unittest.TestCase):
    """Test automatic period discovery from commit dates."""

    def setUp(self):
        self.DiscoveryAnalyzer = _mod.DiscoveryAnalyzer

    def _make_commits(self, date_strings):
        """Helper to create commit dicts with dates."""
        commits = []
        for ds in date_strings:
            commits.append({
                'message': 'some commit',
                'date': datetime.fromisoformat(ds).replace(tzinfo=timezone.utc)
            })
        return commits

    def test_discovers_periods_from_date_range(self):
        """Creates periods spanning the full commit date range."""
        commits = self._make_commits([
            '2010-03-15', '2010-06-20', '2011-01-10',
            '2015-05-01', '2015-08-15', '2016-03-01',
            '2020-01-01', '2020-06-15', '2020-12-01',
        ])
        analyzer = self.DiscoveryAnalyzer(commits)
        periods = analyzer.discover_periods()
        self.assertGreater(len(periods), 1)
        first = list(periods.values())[0]
        self.assertLessEqual(first['start'], '2010-03-15')
        last = list(periods.values())[-1]
        self.assertGreaterEqual(last['end'], '2025-01-01')

    def test_detects_gaps_as_breakpoints(self):
        """A multi-year gap in commits should create a period boundary."""
        commits = self._make_commits([
            '2005-01-15', '2005-06-20', '2005-11-10',
            '2006-02-01', '2006-05-15',
            # 4-year gap
            '2010-03-01', '2010-06-15', '2010-09-01',
            '2011-01-01', '2011-04-15',
        ])
        analyzer = self.DiscoveryAnalyzer(commits)
        periods = analyzer.discover_periods()
        self.assertGreaterEqual(len(periods), 2)

    def test_period_structure(self):
        """Each period has start, end, and description."""
        commits = self._make_commits([
            '2015-01-01', '2016-01-01', '2020-01-01', '2025-01-01'
        ])
        analyzer = self.DiscoveryAnalyzer(commits)
        periods = analyzer.discover_periods()
        for name, data in periods.items():
            self.assertIn('start', data)
            self.assertIn('end', data)
            self.assertIn('description', data)
            self.assertRegex(data['start'], r'\d{4}-\d{2}-\d{2}')
            self.assertRegex(data['end'], r'\d{4}-\d{2}-\d{2}')

    def test_final_period_extends_to_future(self):
        """The last period should extend well beyond the last commit."""
        commits = self._make_commits(['2020-01-01', '2020-06-01', '2025-03-01'])
        analyzer = self.DiscoveryAnalyzer(commits)
        periods = analyzer.discover_periods()
        last_period = list(periods.values())[-1]
        self.assertGreaterEqual(last_period['end'], '2030-01-01')


class TestImportanceDiscovery(unittest.TestCase):
    """Test automatic importance keyword discovery."""

    def setUp(self):
        self.DiscoveryAnalyzer = _mod.DiscoveryAnalyzer

    def test_discovers_arch_keywords_from_themes(self):
        """Extracts architectural keywords from discovered themes."""
        commits = [
            {'message': 'replication sync fix', 'date': None},
            {'message': 'replication changelog update', 'date': None},
            {'message': 'lmdb backend migration', 'date': None},
            {'message': 'lmdb performance tuning', 'date': None},
            {'message': 'openssl certificate handling', 'date': None},
        ]
        analyzer = self.DiscoveryAnalyzer(commits)
        themes = analyzer.discover_themes()
        importance = analyzer.discover_importance_keywords(themes)
        self.assertIn('architectural_keywords', importance)
        self.assertIn('title_keywords', importance)
        self.assertIsInstance(importance['architectural_keywords'], list)
        self.assertIsInstance(importance['title_keywords'], list)

    def test_importance_keywords_not_empty(self):
        """Should produce at least some keywords even with minimal data."""
        commits = [
            {'message': 'database migration', 'date': None},
            {'message': 'database schema update', 'date': None},
        ]
        analyzer = self.DiscoveryAnalyzer(commits)
        themes = analyzer.discover_themes()
        importance = analyzer.discover_importance_keywords(themes)
        self.assertGreater(len(importance['architectural_keywords']), 0)


if __name__ == "__main__":
    unittest.main()
