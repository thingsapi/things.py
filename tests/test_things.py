#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

import unittest
from things import api


DEMO_FILEPATH = "tests/demo.sqlite3"


class ThingsCase(unittest.TestCase):
    """Class documentation goes here."""

    def test_todos(self):
        """Test all todos."""
        todos = api.todos(start="Anytime", filepath=DEMO_FILEPATH)
        self.assertEqual(37, len(todos))
        todos = api.todos(start="Anytime", status="completed", filepath=DEMO_FILEPATH)
        self.assertEqual(1, len(todos))
        todos = api.todos(status="completed", filepath=DEMO_FILEPATH)
        self.assertEqual(3, len(todos))
        with self.assertRaises(ValueError):
            api.todos(status="wrong_value", filepath=DEMO_FILEPATH)

    def test_tags(self):
        """Test all tags."""
        tags = api.tags(filepath=DEMO_FILEPATH)
        self.assertEqual(14, len(tags))

    def test_projects(self):
        """Test all projects."""
        projects = api.projects(filepath=DEMO_FILEPATH)
        self.assertEqual(7, len(projects))

    def test_areas(self):
        """Test all test_areas."""
        test_areas = api.areas(filepath=DEMO_FILEPATH)
        self.assertEqual(1, len(test_areas))


if __name__ == "__main__":
    unittest.main()
