#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

import unittest
from things import api


class ThingsCase(unittest.TestCase):
    """Class documentation goes here."""
        
    def test_tasks(self):
        """Test all tasks."""
        tasks = api.tasks(filepath='tests/demo.sqlite3')
        self.assertEqual(37, len(tasks))
        tasks = api.tasks(status="closed", filepath='tests/demo.sqlite3')
        self.assertEqual(39, len(tasks))

    def test_tags(self):
        """Test all tags."""
        tags = api.tags(filepath='tests/demo.sqlite3')
        self.assertEqual(14, len(tags))

    def test_projects(self):
        """Test all projects."""
        projects = api.projects(filepath='tests/demo.sqlite3')
        self.assertEqual(7, len(projects))

    def test_areas(self):
        """Test all test_areas."""
        test_areas = api.areas(filepath='tests/demo.sqlite3')
        self.assertEqual(1, len(test_areas))


if __name__ == '__main__':
    unittest.main()
