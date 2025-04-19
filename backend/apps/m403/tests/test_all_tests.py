"""
Unified test runner for m403 app – runs models, views, and filter tests.
"""

from apps.m403.tests import test_models, test_views, test_filters
import unittest


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromModule(test_models))
    suite.addTests(loader.loadTestsFromModule(test_views))
    suite.addTests(loader.loadTestsFromModule(test_filters))
    return suite
