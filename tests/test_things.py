#!/usr/bin/env python3

"""Module documentation goes here."""

import contextlib
import io
import os
import sqlite3
import time
import tracemalloc
import unittest
import unittest.mock

import things
import things.database


tracemalloc.start()

TEST_DATABASE_FILEPATH = "tests/main.sqlite"
TEST_DATABASE_FILEPATH_2022 = "tests/db2022/main.sqlite"

THINGSDB = things.database.ENVIRONMENT_VARIABLE_WITH_FILEPATH

# AW: to be continued, helps updating the test expectations when modifying the DB
HEADINGS = 3
INBOX = 2
TRASHED_TODOS = 2
TRASHED_PROJECTS = 1
TRASHED_CANCELLED = 1
TRASHED_COMPLETED = 1
TRASHED_PROJECT_TODOS = 1
TRASHED_PROJECT_TRASHED_TODOS = 1
TRASHED = (
    TRASHED_TODOS
    + TRASHED_PROJECTS
    + TRASHED_CANCELLED
    + TRASHED_COMPLETED
    + TRASHED_PROJECT_TRASHED_TODOS
)
PROJECTS = 4
UPCOMING = 1
DEADLINE_PAST = 3
DEADLINE_FUTURE = 1
DEADLINE = DEADLINE_PAST + DEADLINE_FUTURE
TODAY_PROJECTS = 1
TODAY_TASKS = 4
TODAY = TODAY_PROJECTS + TODAY_TASKS


class ThingsCase(unittest.TestCase):  # noqa: V103 pylint: disable=R0904
    """Class documentation goes here."""

    def setUp(self):
        # Set environment variable to test database
        self.saved_filepath = os.getenv(THINGSDB)
        os.environ[THINGSDB] = TEST_DATABASE_FILEPATH

    def tearDown(self):
        # Restore environment variable to its previous value
        # or delete it if it wasn't set before running the test.
        if self.saved_filepath is None:
            if THINGSDB in os.environ:
                del os.environ[THINGSDB]
        else:
            os.environ[THINGSDB] = self.saved_filepath

    def test_get_tag_by_database_filepath(self):
        del os.environ[THINGSDB]
        tag_uuid = "Qt2AY87x2QDdowSn9HKTt1"
        tag = things.get(tag_uuid, filepath=TEST_DATABASE_FILEPATH)
        self.assertEqual(tag["uuid"], tag_uuid)  # type: ignore

    def test_get_url_scheme_auth_token(self):
        expected = "vKkylosuSuGwxrz7qcklOw"
        token = things.token()
        self.assertEqual(token, expected)

    def test_search(self):
        tasks = things.search("invalid_query")
        self.assertEqual(0, len(tasks))

        # test some special characters
        tasks = things.search("'")
        self.assertEqual(0, len(tasks))

        tasks = things.search('"')
        self.assertEqual(0, len(tasks))

        with self.assertRaises((sqlite3.ProgrammingError, ValueError)):
            things.search("To-Do\0Heading")

        todos = things.search("To-Do % Heading", status=None)
        # Assert finds
        #   "To-Do in Heading",
        #   "Completed To-Do in Heading",
        #   "Canceled To-Do in Heading"
        self.assertEqual(HEADINGS, len(todos))

    def test_inbox(self):
        tasks = things.inbox()
        self.assertEqual(INBOX, len(tasks))

    def test_trashed(self):
        todos = things.todos(trashed=True)
        self.assertEqual(TRASHED_TODOS, len(todos))
        projects = things.projects(trashed=True)
        self.assertEqual(TRASHED_PROJECTS, len(projects))
        projects = things.projects(trashed=None)
        self.assertEqual(PROJECTS, len(projects))
        projects = things.trash(type="project")
        self.assertEqual(TRASHED_PROJECTS, len(projects))
        tasks = things.trash()
        self.assertEqual(TRASHED, len(tasks))

        projects = things.trash(type="project", include_items=True)
        project_items = projects[0]["items"]
        self.assertEqual(TRASHED_PROJECTS, len(project_items))
        filtered_project_items = [
            item for item in project_items if "in Deleted Project" in item["title"]
        ]
        self.assertEqual(TRASHED_PROJECT_TODOS, len(filtered_project_items))

        # TK: Add this test case to the database:
        # to-do with trashed = 1 and whose project also has trashed = 1.
        # AW: These are actually not shown in the GUI
        tasks = things.tasks(type="to-do", trashed=True, context_trashed=True)
        self.assertEqual(0, len(tasks))

    def test_upcoming(self):
        tasks = things.upcoming()
        self.assertEqual(UPCOMING, len(tasks))

    def test_deadlines(self):
        tasks = things.tasks(deadline="past")
        self.assertEqual(DEADLINE_PAST, len(tasks))
        tasks = things.tasks(deadline="future")
        self.assertEqual(DEADLINE_FUTURE, len(tasks))
        tasks = things.deadlines()
        self.assertEqual(DEADLINE, len(tasks))
        with self.assertRaises(ValueError):
            tasks = things.tasks(deadline="invalid_value")

    def test_today(self):
        projects = things.today(type="project")
        self.assertEqual(TODAY_PROJECTS, len(projects))
        tasks = things.today(type="to-do")
        self.assertEqual(TODAY_TASKS, len(tasks))
        tasks = things.today()
        self.assertEqual(TODAY, len(tasks))
        tasks_today = [
            "Upcoming To-Do in Today (yellow)",
            "Project in Today",
            "To-Do in Today",
            "Repeating To-Do",
            "Overdue Todo automatically shown in Today",
        ]
        for count, value in enumerate(tasks_today):
            self.assertEqual(value, tasks[count]["title"])

    def test_checklist(self):
        checklist_items = things.checklist_items("3Eva4XFof6zWb9iSfYy4ej")
        self.assertEqual(3, len(checklist_items))
        checklist_items = things.checklist_items("K9bx7h1xCJdevvyWardZDq")
        self.assertEqual(0, len(checklist_items))

    def test_anytime(self):
        tasks = things.anytime()
        self.assertEqual(14, len(tasks))
        self.assertTrue(any(task.get("area_title") == "Area 1" for task in tasks))

    def test_logbook(self):
        tasks = things.logbook()
        self.assertEqual(23, len(tasks))
        tasks = things.logbook(stop_date=">2099-03-29")
        self.assertEqual(0, len(tasks))
        tasks = things.logbook(stop_date="2021-03-28")
        self.assertEqual(21, len(tasks))
        tasks = things.logbook(stop_date=">=2021-03-27")
        self.assertEqual(23, len(tasks))
        tasks = things.logbook(stop_date="=2021-03-27")
        self.assertEqual(0, len(tasks))

    def test_canceled(self):
        tasks = things.canceled()
        self.assertEqual(11, len(tasks))

    def test_completed(self):
        tasks = things.completed()
        self.assertEqual(12, len(tasks))

    def test_someday(self):
        tasks = things.someday()
        self.assertEqual(1, len(tasks))

    def test_get_by_uuid(self):
        task = things.get("invalid_uuid")
        self.assertEqual(None, task)
        task = things.get("invalid_uuid", "NOT FOUND")
        self.assertEqual("NOT FOUND", task)
        task = things.get("Qt2AY87x2QDdowSn9HKTt1")
        self.assertEqual(4, len(task.keys()))  # type: ignore

    def test_todos(self):
        todos = things.todos(start="Anytime", status="completed")
        self.assertEqual(8, len(todos))
        todos = things.todos(start="Anytime")
        self.assertEqual(10, len(todos))
        todos = things.todos(status="completed")
        self.assertEqual(12, len(todos))
        todos = things.todos(include_items=True)
        self.assertEqual(15, len(todos))
        tasks = things.tasks(include_items=True)
        self.assertEqual(19, len(tasks))
        with self.assertRaises(ValueError):
            things.todos(status="invalid_value")
        todo = things.todos("A2oPvtt4dXoypeoLc8uYzY")
        self.assertEqual(16, len(todo.keys()))  # type: ignore

    def test_tags(self):
        tags = things.tasks(tag="Errand")
        self.assertEqual(1, len(tags))
        tags = things.tags()
        self.assertEqual(5, len(tags))
        tags = things.tags(include_items=True)
        self.assertEqual(5, len(tags))
        tag = things.tags(title="Errand")
        self.assertEqual("Errand", tag["title"])  # type: ignore

        # test tagged items, in particular within headings
        tags = things.tasks(tag="Home")
        self.assertEqual(1, len(tags))
        tasks = things.tasks(project="3x1QqJqfvZyhtw8NSdnZqG")
        self.assertEqual(5, len(tasks))
        tasks = things.tasks(tag="Home", project="3x1QqJqfvZyhtw8NSdnZqG")
        self.assertEqual(1, len(tasks))

    def test_get_link(self):
        link = things.link("uuid")
        self.assertEqual("things:///show?id=uuid", link)

    def test_get_url(self):
        url = things.url("uuid")
        self.assertEqual("things:///show?id=uuid", url)

    def test_get_url_dict(self):
        parameters = {
            "title": "nice_title",
            "list-id": "6c7e77b4-f4d7-44bc-8480-80c0bea585ea",
        }
        url = things.url(command="add", **parameters)
        self.assertEqual(
            "things:///add?title=nice_title&list-id=6c7e77b4-f4d7-44bc-8480-80c0bea585ea",
            url,
        )

    def test_get_url_encoding(self):
        url = things.url(
            command="add",
            title="test task",
            notes="nice notes\nI really like notes",
        )
        self.assertEqual(
            "things:///add?title=test%20task&notes=nice%20notes%0AI%20really%20like%20notes",
            url,
        )

    @unittest.mock.patch("things.api.token")
    def test_get_url_no_token(self, token_mock):
        token_mock.return_value = None
        with self.assertRaises(ValueError):
            # currently only update and update-project require authentication
            things.url(command="update")
        self.assertEqual(token_mock.call_count, 1)

    def test_projects(self):
        projects = things.projects()
        self.assertEqual(3, len(projects))
        projects = things.projects(include_items=True)
        self.assertEqual(5, len(projects[0]["items"]))

    def test_areas(self):
        areas = things.areas()
        self.assertEqual(3, len(areas))
        areas = things.areas(include_items=True)
        self.assertEqual(3, len(areas))
        count = things.areas(count_only=True)
        self.assertEqual(3, count)
        with self.assertRaises(ValueError):
            things.areas("invalid_uuid")
        area = things.areas("Y3JC4XeyGWxzDocQL4aobo")
        self.assertEqual("Area 3", area["title"])  # type: ignore

    def test_database_version(self):
        version = things.Database().get_version()
        self.assertEqual(24, version)

    def test_database_version_mismatch(self):
        os.environ[THINGSDB] = TEST_DATABASE_FILEPATH_2022
        with self.assertRaises(AssertionError):
            things.deadlines()

    def test_last(self):
        last_tasks = things.last("0d")
        self.assertEqual(len(last_tasks), 0)

        last_tasks = things.last("10000w")
        self.assertEqual(len(last_tasks), 19)

        last_tasks = things.last("100y", status="completed")
        self.assertEqual(len(last_tasks), 12)

        with self.assertRaises(ValueError):
            things.last(None)

        with self.assertRaises(ValueError):
            things.last([])

        with self.assertRaises(ValueError):
            things.last("XYZ")

        with self.assertRaises(ValueError):
            things.last("")

        with self.assertRaises(ValueError):
            things.last("3X")

    def test_created_at_date_or_offset(self):
        # for offsets it's the same as last:
        last_tasks = things.tasks(created_at="0d")
        self.assertEqual(len(last_tasks), 0)

        last_tasks = things.tasks(created_at="10000w")
        self.assertEqual(len(last_tasks), 19)

        last_tasks = things.tasks(created_at="100y", status="completed")
        self.assertEqual(len(last_tasks), 12)

        # for offsets it's the same as last:
        last_tasks = things.tasks(created_at="0d")
        self.assertEqual(len(last_tasks), 0)

        last_tasks = things.tasks(created_at="2025-09-29")
        self.assertEqual(len(last_tasks), 0)

        last_tasks = things.tasks(created_at="10000w")
        self.assertEqual(len(last_tasks), 19)

        last_tasks = things.tasks(created_at=">1925-01-01", status="completed")
        self.assertEqual(len(last_tasks), 12)

        last_tasks = things.tasks(created_at=">1825-01-01")
        self.assertEqual(len(last_tasks), 19)

        # None is allowed as it's allowed for dates
        last_tasks = things.tasks(created_at=None)
        self.assertEqual(len(last_tasks), 19)

        # exceptions are also the same as with last:
        with self.assertRaises(TypeError):
            things.tasks(created_at=[])

        with self.assertRaises(ValueError):
            things.tasks(created_at="XYZ")

        with self.assertRaises(ValueError):
            things.tasks(created_at="")

        with self.assertRaises(ValueError):
            things.tasks(created_at="3X")

    def test_tasks(self):
        count = things.tasks(status="completed", last="100y", count_only=True)
        self.assertEqual(count, 12)

        count = things.last("1y", tag="Important", status="completed", count_only=True)
        self.assertEqual(count, 0)

        # get task by uuid
        count = things.tasks(uuid="5pUx6PESj3ctFYbgth1PXY", count_only=True)
        self.assertEqual(count, 1)

        count = things.tasks(uuid="invalid_uuid", count_only=True)
        self.assertEqual(count, 0)

        with self.assertRaises(ValueError):
            things.tasks(uuid="invalid_uuid")

        # special characters
        tasks = things.tasks(area='"')
        self.assertEqual(len(tasks), 0)

        tasks = things.tasks(area="'")
        self.assertEqual(len(tasks), 0)

        with self.assertRaises((sqlite3.ProgrammingError, ValueError)):
            things.tasks(area="\0")

    def test_tasks_stopdate_timezones(self):
        # see https://github.com/thingsapi/things.py/issues/117
        # this test looks at changes to two tasks based on timezone, on either side of midnight UTC

        # make sure we get back both tasks completed for date by midnight UTC+5
        # change timezone to Pakistan
        os.environ["TZ"] = "UTC-5"  # UTC+5, per https://unix.stackexchange.com/a/104091
        time.tzset()
        tasks = things.tasks(
            stop_date="2024-06-18", status="completed", count_only=True
        )
        self.assertEqual(tasks, 2)

        # make sure we get back one task completed for date by midnight UTC
        os.environ["TZ"] = "UTC"
        time.tzset()
        tasks = things.tasks(
            stop_date="2024-06-18", status="completed", count_only=True
        )
        self.assertEqual(tasks, 1)

        # change timezone to New York
        os.environ["TZ"] = "UTC+5"  # UTC-5, per https://unix.stackexchange.com/a/104091
        time.tzset()
        tasks = things.tasks(
            stop_date="2024-06-18", status="completed", count_only=True
        )
        self.assertEqual(tasks, 0)

    def test_database_details(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            things.areas(print_sql=True)
        self.assertTrue("ORDER BY" in output.getvalue())

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            database = things.database.Database()
            database.debug = True
            database.get_tags()
        self.assertTrue("/* Filepath" in output.getvalue())

    @unittest.mock.patch("os.system")
    def test_api_show(self, os_system):
        things.show("invalid_uuid")
        os_system.assert_called_once_with("open 'things:///show?id=invalid_uuid'")

    @unittest.mock.patch("os.system")
    def test_api_complete(self, os_system):
        things.complete("test_uuid")
        os_system.assert_called_once_with(
            "open 'things:///update?id=test_uuid&completed=True&auth-token=vKkylosuSuGwxrz7qcklOw'"
        )

    def test_thingsdate(self):
        sqlfilter: str = things.database.make_thingsdate_filter(
            "deadline", "2021-03-28"
        )
        self.assertEqual("AND deadline == 132464128", sqlfilter)
        sqlfilter = things.database.make_unixtime_filter("stopDate", "future")
        self.assertEqual(
            "AND date(stopDate, 'unixepoch', 'localtime') > date('now', 'localtime')",
            sqlfilter,
        )
        sqlfilter = things.database.make_unixtime_filter("stopDate", False)
        self.assertEqual("AND stopDate IS NULL", sqlfilter)

    def test_thingstime(self):
        test_task = things.tasks("7F4vqUNiTvGKaCUfv5pqYG")
        self.assertEqual(test_task.get("reminder_time"), "12:34")


if __name__ == "__main__":
    unittest.main()
    ThingsCase()  # For Vulture
