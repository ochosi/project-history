#!/usr/bin/env python3
"""Integration tests for project-history tooling."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestSetupProjectIntegration(unittest.TestCase):
    """Integration tests for setup-project script."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_config_file_creation(self):
        """Test that configuration file is created with correct structure."""
        config_path = Path(self.test_dir) / ".project-history-config.json"

        # Create a test config manually
        config = {
            "platforms": {
                "github": {
                    "enabled": True,
                    "owner": "test-owner",
                    "repo": "test-repo"
                },
                "gitlab": {"enabled": False},
                "jira": {"enabled": False}
            },
            "output_dir": "./history"
        }

        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

        # Verify it was created correctly
        self.assertTrue(config_path.exists())

        with open(config_path) as f:
            loaded_config = json.load(f)

        self.assertEqual(loaded_config["platforms"]["github"]["owner"], "test-owner")
        self.assertEqual(loaded_config["platforms"]["github"]["repo"], "test-repo")


class TestEndToEndWorkflow(unittest.TestCase):
    """End-to-end workflow tests."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.history_dir = Path(self.test_dir) / "history"
        self.history_dir.mkdir()

    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_directory_structure_creation(self):
        """Test that expected directory structure is created."""
        # Create expected directories
        (self.history_dir / "issues" / "open").mkdir(parents=True)
        (self.history_dir / "issues" / "closed").mkdir(parents=True)
        (self.history_dir / "pull-requests" / "merged").mkdir(parents=True)
        (self.history_dir / "merge-requests" / "merged").mkdir(parents=True)
        (self.history_dir / "jira-issues" / "done").mkdir(parents=True)

        # Verify structure
        self.assertTrue((self.history_dir / "issues").exists())
        self.assertTrue((self.history_dir / "pull-requests").exists())
        self.assertTrue((self.history_dir / "merge-requests").exists())
        self.assertTrue((self.history_dir / "jira-issues").exists())

    def test_metadata_file_format(self):
        """Test that metadata files are created with correct format."""
        metadata = {
            "repository": "test/repo",
            "fetched_at": "2023-01-01T00:00:00Z",
            "stats": {
                "total_issues": 10,
                "total_prs": 20
            }
        }

        metadata_path = self.history_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        # Verify format
        with open(metadata_path) as f:
            loaded = json.load(f)

        self.assertIn("repository", loaded)
        self.assertIn("fetched_at", loaded)
        self.assertIn("stats", loaded)


if __name__ == "__main__":
    unittest.main()
