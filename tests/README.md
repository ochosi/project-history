# Tests

This directory contains the test suite for the project-history tooling.

## Running Tests

### Run All Tests

```bash
# From repository root
./run_tests.py

# Or with Python
python run_tests.py --verbose
```

### Run Specific Test Files

```bash
# Run only GitHub fetcher tests
python -m unittest tests.test_fetch_github

# Run only GitLab fetcher tests
python -m unittest tests.test_fetch_gitlab

# Run only Jira fetcher tests
python -m unittest tests.test_fetch_jira

# Run only history generator tests
python -m unittest tests.test_generate_history

# Run only integration tests
python -m unittest tests.test_integration
```

### Run Specific Test Cases

```bash
# Run a specific test class
python -m unittest tests.test_fetch_github.TestGitHubHistoryFetcher

# Run a specific test method
python -m unittest tests.test_fetch_github.TestGitHubHistoryFetcher.test_sanitize_filename
```

## Test Coverage

### Unit Tests

- **test_fetch_github.py**: Tests for GitHub fetcher
  - URL parsing (SSH, HTTPS)
  - Filename sanitization
  - Date formatting
  - Markdown generation for issues and PRs

- **test_fetch_gitlab.py**: Tests for GitLab fetcher
  - URL parsing (SSH, HTTPS, self-hosted)
  - Filename sanitization
  - Date formatting
  - Markdown generation for issues and MRs

- **test_fetch_jira.py**: Tests for Jira fetcher
  - Filename sanitization
  - Date formatting
  - Atlassian Document Format (ADF) conversion
  - Markdown generation for tickets

- **test_generate_history.py**: Tests for history generator
  - Multi-platform reference extraction
  - Theme detection
  - Importance scoring
  - Git commit analysis

### Integration Tests

- **test_integration.py**: End-to-end workflow tests
  - Configuration file creation
  - Directory structure creation
  - Metadata file format

## Test Fixtures

The `fixtures/` directory contains mock data for testing:

- `mock_github_data.json` - Sample GitHub issues and PRs
- `mock_gitlab_data.json` - Sample GitLab issues and MRs
- `mock_jira_data.json` - Sample Jira tickets

## Continuous Integration

Tests are automatically run via GitHub Actions on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Manual workflow dispatch

See `.github/workflows/tests.yml` for the CI configuration.

## Writing New Tests

When adding new features:

1. **Add unit tests** for individual functions/methods
2. **Add integration tests** for end-to-end workflows
3. **Update fixtures** if new data formats are needed
4. **Run tests locally** before committing

### Test Template

```python
#!/usr/bin/env python3
"""Tests for new-feature."""

import unittest
from pathlib import Path

class TestNewFeature(unittest.TestCase):
    """Test cases for NewFeature."""

    def setUp(self):
        """Set up test fixtures."""
        pass

    def test_basic_functionality(self):
        """Test basic functionality."""
        result = my_function()
        self.assertEqual(result, expected_value)

    def test_edge_cases(self):
        """Test edge cases."""
        # Test with empty input
        result = my_function("")
        self.assertIsNotNone(result)

        # Test with invalid input
        with self.assertRaises(ValueError):
            my_function(None)

if __name__ == "__main__":
    unittest.main()
```

## Dependencies

Tests require:
- Python 3.8+
- `requests` library
- Standard library modules: `unittest`, `json`, `pathlib`

No additional test frameworks are required.
