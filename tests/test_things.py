#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

import unittest
from things import api


DEMO_FILEPATH = "tests/demo.sqlite3"


class ThingsCase(unittest.TestCase):
    """Class documentation goes here."""

    def test_tasks(self):
        """Test all tasks."""
        tasks = api.tasks(start="Anytime", filepath=DEMO_FILEPATH)
        self.assertEqual(37, len(tasks))
        tasks = api.tasks(start="Anytime", status="completed", filepath=DEMO_FILEPATH)
        self.assertEqual(1, len(tasks))
        tasks = api.tasks(status="completed", filepath=DEMO_FILEPATH)
        self.assertEqual(3, len(tasks))
        # todo: check if this should be possible
        # todo: introduce some sort of strict typing / validation
        tasks = api.tasks(status="wrong_value", filepath=DEMO_FILEPATH)
        self.assertEqual(55, len(tasks))

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
