#!/usr/bin/env python3
"""Test runner for project-history tooling."""

import sys
import unittest
from pathlib import Path

# Add tests directory to path
tests_dir = Path(__file__).parent / "tests"
sys.path.insert(0, str(tests_dir))


def run_tests(verbose=True):
    """Run all tests and return results."""
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = tests_dir
    suite = loader.discover(start_dir, pattern='test_*.py')

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run project-history tests")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Minimal output"
    )

    args = parser.parse_args()

    verbose = not args.quiet
    success = run_tests(verbose=verbose)

    sys.exit(0 if success else 1)
