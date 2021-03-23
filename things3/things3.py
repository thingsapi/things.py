#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simple read-only API for Things 3."""

from __future__ import print_function

__author__ = "Alexander Willner"
__copyright__ = "2020 Alexander Willner"
__credits__ = ["Alexander Willner"]
__license__ = "Apache License 2.0"
__version__ = "2.6.3"
__maintainer__ = "Alexander Willner"
__email__ = "alex@willner.ws"
__status__ = "Development"

import sqlite3
import sys
from random import shuffle
from os import environ, path
import getpass
import configparser
from pathlib import Path


# pylint: disable=R0904,R0902
class Things3():
    """Simple read-only API for Things 3."""

    # Database info
    FILE_CONFIG = str(Path.home()) + '/.kanbanviewrc'
    FILE_DB = '/Library/Group Containers/'\
              'JLMPQHK86H.com.culturedcode.ThingsMac/'\
              'Things Database.thingsdatabase/main.sqlite'
    TABLE_TASK = "TMTask"
    TABLE_AREA = "TMArea"
    TABLE_TAG = "TMTag"
    TABLE_TASKTAG = "TMTaskTag"
    DATE_CREATE = "creationDate"
    DATE_MOD = "userModificationDate"
    DATE_DUE = "dueDate"
    DATE_START = "startDate"
    DATE_STOP = "stopDate"
    IS_INBOX = "start = 0"
    IS_ANYTIME = "start = 1"
    IS_SOMEDAY = "start = 2"
    IS_SCHEDULED = f"{DATE_START} IS NOT NULL"
    IS_NOT_SCHEDULED = f"{DATE_START} IS NULL"
    IS_DUE = f"{DATE_DUE} IS NOT NULL"
    IS_RECURRING = "recurrenceRule IS NOT NULL"
    IS_NOT_RECURRING = "recurrenceRule IS NULL"
    IS_TASK = "type = 0"
    IS_PROJECT = "type = 1"
    IS_HEADING = "type = 2"
    IS_TRASHED = "trashed = 1"
    IS_NOT_TRASHED = "trashed = 0"
    IS_OPEN = "status = 0"
    IS_CANCELLED = "status = 2"
    IS_DONE = "status = 3"
    RECURRING_IS_NOT_PAUSED = "instanceCreationPaused = 0"
    RECURRING_HAS_NEXT_STARTDATE = "nextInstanceStartDate IS NOT NULL"
    MODE_TASK = "type = 0"
    MODE_PROJECT = "type = 1"

    # Variables
    debug = False
    user = getpass.getuser()
    database = f"/Users/{user}/{FILE_DB}"
    filter = ""
    tag_waiting = "Waiting"
    tag_mit = "MIT"
    tag_cleanup = "Cleanup"
    tag_a = "A"
    tag_b = "B"
    tag_c = "C"
    tag_d = "D"
    stat_days = 365
    anonymize = False
    config = configparser.ConfigParser()
    config.read(FILE_CONFIG)

    # pylint: disable=R0913
    def __init__(self,
                 database=None,
                 tag_waiting=None,
                 tag_mit=None,
                 tag_cleanup=None,
                 tag_a=None,
                 tag_b=None,
                 tag_c=None,
                 tag_d=None,
                 stat_days=None,
                 anonymize=None):

        cfg = self.get_from_config(tag_waiting, 'TAG_WAITING')
        self.tag_waiting = cfg if cfg else self.tag_waiting
        self.set_config('TAG_WAITING', self.tag_waiting)

        cfg = self.get_from_config(anonymize, 'ANONYMIZE')
        self.anonymize = (cfg == 'True') if (cfg == 'True') else self.anonymize
        self.set_config('ANONYMIZE', self.anonymize)

        cfg = self.get_from_config(tag_mit, 'TAG_MIT')
        self.tag_mit = cfg if cfg else self.tag_mit
        self.set_config('TAG_MIT', self.tag_mit)

        cfg = self.get_from_config(tag_cleanup, 'TAG_CLEANUP')
        self.tag_cleanup = cfg if cfg else self.tag_cleanup
        self.set_config('TAG_CLEANUP', self.tag_cleanup)

        cfg = self.get_from_config(tag_a, 'TAG_A')
        self.tag_a = cfg if cfg else self.tag_a
        self.set_config('TAG_A', self.tag_a)

        cfg = self.get_from_config(tag_b, 'TAG_B')
        self.tag_b = cfg if cfg else self.tag_b
        self.set_config('TAG_B', self.tag_b)

        cfg = self.get_from_config(tag_c, 'TAG_C')
        self.tag_c = cfg if cfg else self.tag_c
        self.set_config('TAG_C', self.tag_c)

        cfg = self.get_from_config(tag_d, 'TAG_D')
        self.tag_d = cfg if cfg else self.tag_d
        self.set_config('TAG_D', self.tag_d)

        cfg = self.get_from_config(stat_days, 'STAT_DAYS')
        self.stat_days = cfg if cfg else self.stat_days
        self.set_config('STAT_DAYS', self.stat_days)

        cfg = self.get_from_config(database, 'THINGSDB')
        self.database = cfg if cfg else self.database
        # Automated migration to new database location in Things 3.12.6/3.13.1
        # --------------------------------
        try:
            with open(self.database) as f_d:
                if "Your database file has been moved there" in f_d.readline():
                    self.database = f"/Users/{self.user}/{self.FILE_DB}"
        except (UnicodeDecodeError, FileNotFoundError, PermissionError):
            pass  # binary file (old database) or doesn't exist
        # --------------------------------
        self.set_config('THINGSDB', self.database)

    def set_config(self, key, value, domain='DATABASE'):
        """Write variable to config."""
        if domain not in self.config:
            self.config.add_section(domain)
        if value is not None and key is not None:
            self.config.set(domain, str(key), str(value))
            with open(self.FILE_CONFIG, "w+") as configfile:
                self.config.write(configfile)

    def get_config(self, key, domain='DATABASE'):
        """Get variable from config."""
        result = None
        if domain in self.config and key in self.config[domain]:
            result = path.expanduser(self.config[domain][key])
        return result

    def get_from_config(self, variable, key, domain='DATABASE'):
        """Set variable. Priority: input, environment, config"""
        result = None
        if variable is not None:
            result = variable
        elif environ.get(key):
            result = environ.get(key)
        elif domain in self.config and key in self.config[domain]:
            result = path.expanduser(self.config[domain][key])
        return result

    @staticmethod
    def anonymize_string(string):
        """Scramble text."""
        if string is None:
            return None
        string = list(string)
        shuffle(string)
        string = ''.join(string)
        return string

    @staticmethod
    def dict_factory(cursor, row):
        """Convert SQL result into a dictionary"""
        dictionary = {}
        for idx, col in enumerate(cursor.description):
            dictionary[col[0]] = row[idx]
        return dictionary

    def anonymize_tasks(self, tasks):
        """Scramble output for screenshots."""
        if self.anonymize:
            for task in tasks:
                task['title'] = self.anonymize_string(task['title'])
                task['context'] = self.anonymize_string(
                    task['context']) if 'context' in task else ''
        return tasks

    def get_inbox(self):
        """Get all tasks from the inbox."""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_OPEN} AND
                TASK.{self.IS_INBOX}
                ORDER BY TASK.duedate DESC , TASK.todayIndex
                """
        return self.get_rows(query)

    def get_today(self):
        """Get all tasks from the todays list."""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_OPEN} AND
                (TASK.{self.IS_ANYTIME} OR (
                     TASK.{self.IS_SOMEDAY} AND
                     TASK.{self.DATE_START} <= strftime('%s', 'now')
                     )
                ) AND
                TASK.{self.IS_SCHEDULED} AND (
                    (
                        PROJECT.title IS NULL OR (
                            PROJECT.{self.IS_NOT_TRASHED}
                        )
                    ) AND (
                        HEADPROJ.title IS NULL OR (
                            HEADPROJ.{self.IS_NOT_TRASHED}
                        )
                    )
                )
                ORDER BY TASK.duedate DESC , TASK.todayIndex
                """
        return self.get_rows(query)

    def get_task(self, area=None, project=None):
        """Get tasks."""
        afilter = f'AND TASK.area = "{area}"' \
            if area is not None else ''
        pfilter = f'AND TASK.project = "{project}"' \
            if project is not None else ''
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_OPEN} AND
                TASK.{self.IS_ANYTIME} AND
                TASK.{self.IS_NOT_RECURRING} AND (
                    (
                        PROJECT.title IS NULL OR (
                            PROJECT.{self.IS_NOT_TRASHED}
                        )
                    ) AND (
                        HEADPROJ.title IS NULL OR (
                            HEADPROJ.{self.IS_NOT_TRASHED}
                        )
                    )
                )
                {afilter}
                {pfilter}
                ORDER BY TASK.duedate DESC, TASK.{self.DATE_CREATE} DESC
                """
        return self.get_rows(query)

    def get_someday(self):
        """Get someday tasks."""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_OPEN} AND
                TASK.{self.IS_SOMEDAY} AND
                TASK.{self.IS_NOT_SCHEDULED} AND
                TASK.{self.IS_NOT_RECURRING} AND (
                    (
                        PROJECT.title IS NULL OR (
                            PROJECT.{self.IS_NOT_TRASHED}
                        )
                    ) AND (
                        HEADPROJ.title IS NULL OR (
                            HEADPROJ.{self.IS_NOT_TRASHED}
                        )
                    )
                )
                ORDER BY TASK.duedate DESC, TASK.{self.DATE_CREATE} DESC
                """
        return self.get_rows(query)

    def get_upcoming(self):
        """Get upcoming tasks."""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_OPEN} AND
                TASK.{self.IS_SOMEDAY} AND
                TASK.{self.IS_SCHEDULED} AND
                TASK.{self.IS_NOT_RECURRING} AND (
                    (
                        PROJECT.title IS NULL OR (
                            PROJECT.{self.IS_NOT_TRASHED}
                        )
                    ) AND (
                        HEADPROJ.title IS NULL OR (
                            HEADPROJ.{self.IS_NOT_TRASHED}
                        )
                    )
                )
                ORDER BY TASK.startdate, TASK.todayIndex
                """
        return self.get_rows(query)

    def get_waiting(self):
        """Get waiting tasks."""
        return self.get_tag(self.tag_waiting)

    def get_mit(self):
        """Get most important tasks."""
        return self.get_tag(self.tag_mit)

    def get_tag(self, tag):
        """Get task with specific tag"""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_OPEN} AND
                TASK.{self.IS_NOT_RECURRING} AND
                TAGS.tags=(SELECT uuid FROM {self.TABLE_TAG}
                             WHERE title='{tag}'
                          )
                AND (
                    (
                        PROJECT.title IS NULL OR (
                            PROJECT.{self.IS_NOT_TRASHED}
                        )
                    ) AND (
                        HEADPROJ.title IS NULL OR (
                            HEADPROJ.{self.IS_NOT_TRASHED}
                        )
                    )
                )
                ORDER BY TASK.duedate DESC , TASK.todayIndex
                """
        return self.get_rows(query)

    def get_tag_today(self, tag):
        """Get today tasks with specific tag"""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_OPEN} AND
                (TASK.{self.IS_ANYTIME} OR (
                     TASK.{self.IS_SOMEDAY} AND
                     TASK.{self.DATE_START} <= strftime('%s', 'now')
                     )
                ) AND
                TAGS.tags=(SELECT uuid FROM {self.TABLE_TAG}
                             WHERE title='{tag}') AND
                TASK.{self.IS_SCHEDULED} AND (
                    (
                        PROJECT.title IS NULL OR (
                            PROJECT.{self.IS_NOT_TRASHED}
                        )
                    ) AND (
                        HEADPROJ.title IS NULL OR (
                            HEADPROJ.{self.IS_NOT_TRASHED}
                        )
                    )
                )
                ORDER BY TASK.duedate DESC , TASK.todayIndex
            """
        return self.get_rows(query)

    def get_anytime(self):
        """Get anytime tasks."""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_OPEN} AND
                TASK.{self.IS_ANYTIME} AND
                TASK.{self.IS_NOT_SCHEDULED} AND (
                    (
                        PROJECT.title IS NULL OR (
                            PROJECT.{self.IS_ANYTIME} AND
                            PROJECT.{self.IS_NOT_SCHEDULED} AND
                            PROJECT.{self.IS_NOT_TRASHED}
                        )
                    ) AND (
                        HEADPROJ.title IS NULL OR (
                            HEADPROJ.{self.IS_ANYTIME} AND
                            HEADPROJ.{self.IS_NOT_SCHEDULED} AND
                            HEADPROJ.{self.IS_NOT_TRASHED}
                        )
                    )
                )
                ORDER BY TASK.duedate DESC , TASK.todayIndex
                """
        if self.filter:
            # ugly hack for Kanban task view on project
            query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_OPEN} AND
                TASK.{self.IS_ANYTIME} AND
                TASK.{self.IS_NOT_SCHEDULED} AND (
                    (
                        PROJECT.title IS NULL OR (
                            PROJECT.{self.IS_NOT_TRASHED}
                        )
                    ) AND (
                        HEADPROJ.title IS NULL OR (
                            HEADPROJ.{self.IS_NOT_TRASHED}
                        )
                    )
                )
                ORDER BY TASK.duedate DESC , TASK.todayIndex
                """
        return self.get_rows(query)

    def get_completed(self):
        """Get completed tasks."""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_DONE}
                ORDER BY TASK.{self.DATE_STOP}
                """
        return self.get_rows(query)

    def get_cancelled(self):
        """Get cancelled tasks."""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_CANCELLED}
                ORDER BY TASK.{self.DATE_STOP}
                """
        return self.get_rows(query)

    def get_trashed(self):
        """Get trashed tasks."""
        query = f"""
                TASK.{self.IS_TRASHED} AND
                TASK.{self.IS_TASK}
                ORDER BY TASK.{self.DATE_STOP}
                """
        return self.get_rows(query)

    def get_projects(self, area=None):
        """Get projects."""
        afilter = f'AND TASK.area = "{area}"' if area is not None else ''
        query = f"""
                SELECT
                    TASK.uuid,
                    TASK.title,
                    NULL as context,
                    (SELECT COUNT(uuid)
                     FROM TMTask AS PROJECT_TASK
                     WHERE
                       PROJECT_TASK.project = TASK.uuid AND
                       PROJECT_TASK.{self.IS_NOT_TRASHED} AND
                       PROJECT_TASK.{self.IS_OPEN}
                    ) AS size
                FROM
                    {self.TABLE_TASK} AS TASK
                WHERE
                    TASK.{self.IS_NOT_TRASHED} AND
                    TASK.{self.IS_PROJECT} AND
                    TASK.{self.IS_OPEN}
                    {afilter}
                ORDER BY TASK.title COLLATE NOCASE
                """
        return self.execute_query(query)

    def get_areas(self):
        """Get areas."""
        query = f"""
                SELECT
                    AREA.uuid AS uuid,
                    AREA.title AS title,
                    (SELECT COUNT(uuid)
                        FROM TMTask AS PROJECT
                        WHERE
                        PROJECT.area = AREA.uuid AND
                        PROJECT.{self.IS_NOT_TRASHED} AND
                        PROJECT.{self.IS_OPEN}
                    ) AS size
                FROM
                    {self.TABLE_AREA} AS AREA
                ORDER BY AREA.title COLLATE NOCASE
                """
        return self.execute_query(query)

    def get_all(self):
        """Get all tasks."""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND (
                    (
                        PROJECT.title IS NULL OR (
                            PROJECT.{self.IS_NOT_TRASHED}
                        )
                    ) AND (
                        HEADPROJ.title IS NULL OR (
                            HEADPROJ.{self.IS_NOT_TRASHED}
                        )
                    )
                )
                """
        return self.get_rows(query)

    def get_due(self):
        """Get due tasks."""
        query = f"""
                TASK.{self.IS_NOT_TRASHED} AND
                TASK.{self.IS_TASK} AND
                TASK.{self.IS_OPEN} AND
                TASK.{self.IS_DUE} AND (
                    (
                        PROJECT.title IS NULL OR (
                            PROJECT.{self.IS_NOT_TRASHED}
                        )
                    ) AND (
                        HEADPROJ.title IS NULL OR (
                            HEADPROJ.{self.IS_NOT_TRASHED}
                        )
                    )
                )
                ORDER BY TASK.{self.DATE_DUE}
                """
        return self.get_rows(query)

    def get_lint(self):
        """Get tasks that float around"""
        query = f"""
            TASK.{self.IS_NOT_TRASHED} AND
            TASK.{self.IS_OPEN} AND
            TASK.{self.IS_TASK} AND
            (TASK.{self.IS_SOMEDAY} OR TASK.{self.IS_ANYTIME}) AND
            TASK.project IS NULL AND
            TASK.area IS NULL AND
            TASK.actionGroup IS NULL
            """
        return self.get_rows(query)

    def get_empty_projects(self):
        """Get projects that are empty"""
        query = f"""
            TASK.{self.IS_NOT_TRASHED} AND
            TASK.{self.IS_OPEN} AND
            TASK.{self.IS_PROJECT} AND
            TASK.{self.IS_ANYTIME}
            GROUP BY TASK.uuid
            HAVING
                (SELECT COUNT(uuid)
                 FROM TMTask AS PROJECT_TASK
                 WHERE
                   PROJECT_TASK.project = TASK.uuid AND
                   PROJECT_TASK.{self.IS_NOT_TRASHED} AND
                   PROJECT_TASK.{self.IS_OPEN} AND
                   (PROJECT_TASK.{self.IS_ANYTIME} OR
                    PROJECT_TASK.{self.IS_SCHEDULED} OR
                      (PROJECT_TASK.{self.IS_RECURRING} AND
                       PROJECT_TASK.{self.RECURRING_IS_NOT_PAUSED} AND
                       PROJECT_TASK.{self.RECURRING_HAS_NEXT_STARTDATE}
                      )
                   )
                ) = 0
            """
        return self.get_rows(query)

    def get_largest_projects(self):
        """Get projects that are empty"""
        query = f"""
            SELECT
                TASK.uuid,
                TASK.title AS title,
                {self.DATE_CREATE} AS created,
                {self.DATE_MOD} AS modified,
                (SELECT COUNT(uuid)
                 FROM TMTask AS PROJECT_TASK
                 WHERE
                   PROJECT_TASK.project = TASK.uuid AND
                   PROJECT_TASK.{self.IS_NOT_TRASHED} AND
                   PROJECT_TASK.{self.IS_OPEN}
                ) AS tasks
            FROM
                {self.TABLE_TASK} AS TASK
            WHERE
               TASK.{self.IS_NOT_TRASHED} AND
               TASK.{self.IS_OPEN} AND
               TASK.{self.IS_PROJECT}
            GROUP BY TASK.uuid
            ORDER BY tasks COLLATE NOCASE DESC
            """
        return self.execute_query(query)

    def get_daystats(self):
        """Get a history of task activities"""
        query = f"""
                WITH RECURSIVE timeseries(x) AS (
                    SELECT 0
                    UNION ALL
                    SELECT x+1 FROM timeseries
                    LIMIT {self.stat_days}
                )
                SELECT
                    date(julianday("now", "-{self.stat_days} days"),
                         "+" || x || " days") as date,
                    CREATED.TasksCreated as created,
                    CLOSED.TasksClosed as completed,
                    CANCELLED.TasksCancelled as cancelled,
                    TRASHED.TasksTrashed as trashed
                FROM timeseries
                LEFT JOIN
                    (SELECT COUNT(uuid) AS TasksCreated,
                        date({self.DATE_CREATE},"unixepoch") AS DAY
                        FROM {self.TABLE_TASK} AS TASK
                        WHERE DAY NOT NULL
                          AND TASK.{self.IS_TASK}
                        GROUP BY DAY)
                    AS CREATED ON CREATED.DAY = date
                LEFT JOIN
                    (SELECT COUNT(uuid) AS TasksCancelled,
                        date(stopDate,"unixepoch") AS DAY
                        FROM {self.TABLE_TASK} AS TASK
                        WHERE DAY NOT NULL
                          AND TASK.{self.IS_CANCELLED} AND TASK.{self.IS_TASK}
                        GROUP BY DAY)
                        AS CANCELLED ON CANCELLED.DAY = date
                LEFT JOIN
                    (SELECT COUNT(uuid) AS TasksTrashed,
                        date({self.DATE_MOD},"unixepoch") AS DAY
                        FROM {self.TABLE_TASK} AS TASK
                        WHERE DAY NOT NULL
                          AND TASK.{self.IS_TRASHED} AND TASK.{self.IS_TASK}
                        GROUP BY DAY)
                        AS TRASHED ON TRASHED.DAY = date
                LEFT JOIN
                    (SELECT COUNT(uuid) AS TasksClosed,
                        date(stopDate,"unixepoch") AS DAY
                        FROM {self.TABLE_TASK} AS TASK
                        WHERE DAY NOT NULL
                          AND TASK.{self.IS_DONE} AND TASK.{self.IS_TASK}
                        GROUP BY DAY)
                        AS CLOSED ON CLOSED.DAY = date
                """
        return self.execute_query(query)

    def get_minutes_today(self):
        """Count the planned minutes for today."""
        query = f"""
                SELECT
                    SUM(TAG.title) AS minutes
                FROM
                    {self.TABLE_TASK} AS TASK
                LEFT OUTER JOIN
                TMTask PROJECT ON TASK.project = PROJECT.uuid
                LEFT OUTER JOIN
                    TMArea AREA ON TASK.area = AREA.uuid
                LEFT OUTER JOIN
                    TMTask HEADING ON TASK.actionGroup = HEADING.uuid
                LEFT OUTER JOIN
                    TMTask HEADPROJ ON HEADING.project = HEADPROJ.uuid
                LEFT OUTER JOIN
                    TMTaskTag TAGS ON TASK.uuid = TAGS.tasks
                LEFT OUTER JOIN
                    TMTag TAG ON TAGS.tags = TAG.uuid
                WHERE
                    printf("%d", TAG.title) = TAG.title AND
                    TASK.{self.IS_NOT_TRASHED} AND
                    TASK.{self.IS_TASK} AND
                    TASK.{self.IS_OPEN} AND
                    TASK.{self.IS_ANYTIME} AND
                    TASK.{self.IS_SCHEDULED} AND (
                        (
                            PROJECT.title IS NULL OR (
                                PROJECT.{self.IS_NOT_TRASHED}
                            )
                        ) AND (
                            HEADPROJ.title IS NULL OR (
                                HEADPROJ.{self.IS_NOT_TRASHED}
                            )
                        )
                    )
                """
        return self.execute_query(query)

    def get_cleanup(self):
        """Tasks and projects that need work."""
        result = []
        result.extend(self.get_lint())
        result.extend(self.get_empty_projects())
        result.extend(self.get_tag(self.tag_cleanup))
        result = [i for n, i in enumerate(result) if i not in result[n + 1:]]
        return result

    @staticmethod
    def get_not_implemented():
        """Not implemented warning."""
        return [{"title": "not implemented"}]

    def get_rows(self, sql):
        """Query Things database."""

        sql = f"""
            SELECT DISTINCT
                TASK.uuid,
                TASK.title,
                CASE
                    WHEN AREA.title IS NOT NULL THEN AREA.title
                    WHEN PROJECT.title IS NOT NULL THEN PROJECT.title
                    WHEN HEADING.title IS NOT NULL THEN HEADING.title
                END AS context,
                CASE
                    WHEN AREA.uuid IS NOT NULL THEN AREA.uuid
                    WHEN PROJECT.uuid IS NOT NULL THEN PROJECT.uuid
                END AS context_uuid,
                CASE
                    WHEN TASK.recurrenceRule IS NULL
                    THEN strftime('%d.%m.', TASK.dueDate,"unixepoch") ||
                         substr(strftime('%Y', TASK.dueDate,"unixepoch"),3, 2)
                ELSE NULL
                END AS due,
                date(TASK.{self.DATE_CREATE},"unixepoch") as created,
                date(TASK.{self.DATE_MOD},"unixepoch") as modified,
                strftime('%d.%m.', TASK.startDate,"unixepoch") ||
                  substr(strftime('%Y', TASK.startDate,"unixepoch"),3, 2)
                  as started,
                date(TASK.stopDate,"unixepoch") as stopped,
                (SELECT COUNT(uuid)
                 FROM TMTask AS PROJECT_TASK
                 WHERE
                   PROJECT_TASK.project = TASK.uuid AND
                   PROJECT_TASK.{self.IS_NOT_TRASHED} AND
                   PROJECT_TASK.{self.IS_OPEN}
                ) AS size,
                CASE
                    WHEN TASK.{self.IS_TASK} THEN 'task'
                    WHEN TASK.{self.IS_PROJECT} THEN 'project'
                    WHEN TASK.{self.IS_HEADING} THEN 'heading'
                END AS type,
                TASK.notes
            FROM
                {self.TABLE_TASK} AS TASK
            LEFT OUTER JOIN
                {self.TABLE_TASK} PROJECT ON TASK.project = PROJECT.uuid
            LEFT OUTER JOIN
                {self.TABLE_AREA} AREA ON TASK.area = AREA.uuid
            LEFT OUTER JOIN
                {self.TABLE_TASK} HEADING ON TASK.actionGroup = HEADING.uuid
            LEFT OUTER JOIN
                {self.TABLE_TASK} HEADPROJ ON HEADING.project = HEADPROJ.uuid
            LEFT OUTER JOIN
                {self.TABLE_TASKTAG} TAGS ON TASK.uuid = TAGS.tasks
            LEFT OUTER JOIN
                {self.TABLE_TAG} TAG ON TAGS.tags = TAG.uuid
            WHERE
                {self.filter}
                {sql}
                """

        return self.execute_query(sql)

    def execute_query(self, sql):
        """Run the actual query"""
        if self.debug is True:
            print(self.database)
            print(sql)
        try:
            connection = sqlite3.connect(
                'file:' + self.database + '?mode=ro', uri=True)
            connection.row_factory = Things3.dict_factory
            cursor = connection.cursor()
            cursor.execute(sql)
            tasks = cursor.fetchall()
            tasks = self.anonymize_tasks(tasks)
            if self.debug:
                for task in tasks:
                    print(task)
            return tasks
        except sqlite3.OperationalError as error:
            print(f"Could not query the database at: {self.database}.")
            print(f"Details: {error}.")
            sys.exit(2)

    # pylint: disable=C0103
    def mode_project(self):
        """Hack to switch to project view"""
        self.IS_TASK = self.MODE_PROJECT

    # pylint: disable=C0103
    def mode_task(self):
        """Hack to switch to project view"""
        self.IS_TASK = self.MODE_TASK

    functions = {
        "inbox": get_inbox,
        "today": get_today,
        "next": get_anytime,
        "backlog": get_someday,
        "upcoming": get_upcoming,
        "waiting": get_waiting,
        "mit": get_mit,
        "completed": get_completed,
        "cancelled": get_cancelled,
        "trashed": get_trashed,
        "projects": get_projects,
        "areas": get_areas,
        "all": get_all,
        "due": get_due,
        "lint": get_lint,
        "empty": get_empty_projects,
        "cleanup": get_cleanup,
        "top-proj": get_largest_projects,
        "stats-day": get_daystats,
        "stats-min-today": get_minutes_today
    }
