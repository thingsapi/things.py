#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

import unittest
from things import api


DEMO_FILEPATH = "tests/main.sqlite"


class ThingsCase(unittest.TestCase):
    """Class documentation goes here."""

    def test_inbox(self):
        """Test inbox."""
        tasks = api.inbox(filepath=DEMO_FILEPATH)
        self.assertEqual(1, len(tasks))

    def test_upcoming(self):
        """Test upcoming."""
        tasks = api.upcoming(filepath=DEMO_FILEPATH)
        self.assertEqual(2, len(tasks))

    def test_due(self):
        """Test due."""
        tasks = api.due(filepath=DEMO_FILEPATH)
        self.assertEqual(1, len(tasks))

    def test_today(self):
        """Test today."""
        tasks = api.today(filepath=DEMO_FILEPATH)
        self.assertEqual(1, len(tasks))

    def test_get(self):
        """Test get."""
        tasks = api.get('wrong_uuid', filepath=DEMO_FILEPATH)
        self.assertEqual(None, tasks)

    def test_todos(self):
        """Test all tasks."""
        tasks = api.todos(start="Anytime", filepath=DEMO_FILEPATH)
        self.assertEqual(5, len(tasks))
        tasks = api.todos(start="Anytime", status="completed", filepath=DEMO_FILEPATH)
        self.assertEqual(6, len(tasks))
        tasks = api.todos(status="completed", filepath=DEMO_FILEPATH)
        self.assertEqual(10, len(tasks))
        tasks = api.todos(include_items=True, filepath=DEMO_FILEPATH)
        self.assertEqual(9, len(tasks))
        with self.assertRaises(ValueError):
            api.todos(status="wrong_value", filepath=DEMO_FILEPATH)
        tasks = api.tasks('A2oPvtt4dXoypeoLc8uYzY', filepath=DEMO_FILEPATH)
        self.assertEqual(13, len(tasks))

    def test_tags(self):
        """Test all tags."""
        tags = api.tags(filepath=DEMO_FILEPATH)
        self.assertEqual(5, len(tags))

    def test_projects(self):
        """Test all projects."""
        projects = api.projects(filepath=DEMO_FILEPATH)
        self.assertEqual(2, len(projects))

    def test_areas(self):
        """Test all test_areas."""
        test_areas = api.areas(filepath=DEMO_FILEPATH)
        self.assertEqual(1, len(test_areas))


if __name__ == "__main__":
    unittest.main()
