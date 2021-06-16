"""
Module implementing the Things API.

The terms of the API aim to match those used in the Things app and
Things URL Scheme. In some specific cases we instead choose to use terms
that occur in the Things SQL database to closer reflect its underlying
data structures. Whenever that happens, we define the new term here.
"""

import os
from shlex import quote
from typing import Dict, List, Union

from things.database import Database


# --------------------------------------------------
# Core functions
# --------------------------------------------------


def tasks(uuid=None, include_items=False, **kwargs):  # noqa: C901
    """
    Read tasks into dicts.

    Note: "task" is a technical term used in the database to refer to a
    to-do, project, or heading. For details, check the "type"-parameter.

    Per default, only tasks marked as incomplete are included. If you
    want to include completed or canceled tasks in the result, check the
    "status"-parameter.

    Parameters
    ----------
    uuid : str or None, optional
        Any valid task uuid. If None, then return all tasks matched.

    include_items : bool, default False
        Include items contained within a task. These might include
        checklist items, headings, and to-dos.

    type : {'to-do', 'heading', 'project', None}, optional
        Only return a specific type of task:
        - `'to-do'`:    may have a checklist; may be in an area and have tags.
        - `'project'`:  may have to-dos and headings; may be in an area and
                        have tags.
        - `'heading'`:  part of a project; groups tasks.
        - `None` (default): return all types of tasks.

    status : {'incomplete', 'completed', 'canceled', None}, optional, \
        default 'incomplete'

        Only include tasks matching that status. If `status == None`,
        then include tasks with any status value.

    start : {'Inbox', 'Anytime', 'Someday', None}, optional
        Only include tasks matching that start value. If the argument is
        `None` (default), then include tasks with any start value.

    area : str or bool or None, optional
        Any valid uuid of an area. Only include tasks matching that area.
        Special cases:
        - `area == False`, only include tasks _without_ an area.
        - `area == True`, only include tasks _with_ an area.
        - `area == None` (default), then include all tasks.

    project : str or bool or None, optional
        Any valid uuid of a project. Only include tasks matching that project.
        Special cases:
        - `project == False`, only include tasks _without_ a project.
        - `project == True`, only include tasks _with_ a project.
        - `project == None` (default), then include all tasks.

    heading : str or None, optional
        Any valid uuid of a heading. Only include tasks matching that heading.
        Special cases:
        - `heading == False`, only include tasks _without_ a heading.
        - `heading == True`, only include tasks _with_ a heading.
        - `heading == None` (default), then include all tasks.

    tag : str or bool or None, optional
        Any valid title of a tag. Only include tasks matching that tag.
        Special cases:
        - `tag == False`, only include tasks _without_ tags.
        - `tag == True`, only include tasks _with_ tags.
        - `tag == None` (default), then include all tasks.

    start_date : bool, str or None, optional
        - `start_date == False`, only include tasks _without_ a start date.
        - `start_date == True`, only include tasks with a start date.
        - `start_date == 'future'`, only include tasks with a future start date.
        - `start_date == 'past'`, only include tasks with a past start date.
          Note: this includes today's date.
        - `start_date == None` (default), then include all tasks.

    deadline : bool, str or None, optional
        - `deadline == False`, only include tasks _without_ a deadline.
        - `deadline == True`, only include tasks _with_ a deadline.
        - `deadline == 'future'`, only include tasks with a future deadline.
        - `deadline == 'past'`, only include tasks with a past deadline.
          Note: this includes today's date.
        - `deadline == None` (default), then include all tasks.

    deadline_suppressed : bool or None, optional
        "deadline suppressed" is a technical term used in the database.
        When tasks have an overdue deadline they show up in Today.
        Some of us "suppress" some tasks, that is, move them out of
        Today and into Inbox, Anytime, or Someday. For those moved tasks
        the deadline is said to be suppressed.
        - `deadline_suppressed == True`, only include tasks with deadlines
          and whose deadlines have been suppressed.
        - `deadline_suppressed == False`, include any task _except_ those
          with suppressed deadlines.
        - `deadline_suppressed == None` (default), include any task.

    trashed : bool or None, optional, default False
        - `trashed == False` (default), only include non-trashed tasks.
        - `trashed == True`, only include trashed tasks.
        - `trashed == None`, include both kind of tasks.

    context_trashed : bool or None, optional, default False
        Some tasks may be within a context of a project or a heading.
        This manages how to handle such tasks. The other tasks are not
        affected by this setting.

        - `context_trashed == False` (default), for tasks within a context,
           only return tasks whose context has _not_ been trashed.
        - `context_trashed == True`, for tasks within a context,
           only return tasks whose context has been trashed.
        - `context_trashed == None`, include both kind of tasks.

    last : str, optional
        Limit returned tasks to tasks created within the last X days,
        weeks, or years. For example: '3d', '5w', or '1y'.

        Takes as input an offset string of the format 'X[d/w/y]' where X
        is a non-negative  integer that is followed by 'd', 'w', or 'y'
        which stand for 'days', 'weeks', and 'years', respectively.

    search_query : str, optional
        The string value is passed to the SQL LIKE operator. It can thus
        include placeholders such as '%' and '_'. Per default, it is
        wrapped in '% ... %'.

        Currently titles and notes of to-dos, projects, headings, and areas
        are taken into account.

    index : {'index', 'todayIndex'}, default 'index'
        Database field to order result by.

    count_only : bool, default False
        Only output length of result. This is done by a SQL COUNT query.

    print_sql : bool, default False
        Print every SQL query performed. Some may contain '?' and ':'
        characters, which correspond to SQLite parameter tokens.
        See https://www.sqlite.org/lang_expr.html#varparam

    filepath : str, optional
        Any valid path of a SQLite database file generated by the Things app.
        If the environment variable `THINGSDB` is set, then use that path.
        Otherwise, access the default database path.

    database : things.database.Database, optional
        Any valid database object previously instantiated.

    Returns
    -------
    list of dict (default)
        Representing multiple tasks.
    dict (if `uuid` is given)
        Representing a single task.
    int (`count_only == True`)
        Count of matching Tasks.

    Examples
    --------
    >>> things.tasks()
    [{'uuid': '6Hf2qWBjWhq7B1xszwdo34', 'type': 'to-do', 'title':...
    >>> things.tasks('DfYoiXcNLQssk9DkSoJV3Y')
    {'uuid': 'DfYoiXcNLQssk9DkSoJV3Y', 'type': 'to-do', 'title': ...
    >>> things.tasks(area='hIo1FJlAYGKt1Yj38vzKc3', include_items=True)
    []
    >>> things.tasks(status='completed', count_only=True)
    10
    >>> things.tasks(status='completed', last='1w', count_only=True)
    0

    """
    database = pop_database(kwargs)
    result = database.get_tasks(
        uuid=uuid, status=kwargs.pop("status", "incomplete"), **kwargs
    )

    if kwargs.get("count_only"):
        return result

    # overwrite `include_items` if fetching a single task.
    if uuid:
        include_items = True

    for task in result:
        # TK: How costly of an operation is it to do this for every task?
        # IF costly, then can it be made significantly more efficient
        # by optimizing SQL calls?

        if task.get("tags"):
            task["tags"] = database.get_tags(task=task["uuid"])

        if not include_items:
            continue

        # include items
        if task["type"] == "to-do":
            if task.get("checklist"):
                task["checklist"] = database.get_checklist_items(task["uuid"])
        elif task["type"] == "project":
            project = task
            project["items"] = items = tasks(
                project=project["uuid"],
                context_trashed=None,
                include_items=True,
                database=database,
            )
            # to-dos without headings appear before headings in app
            items.sort(key=lambda item: item["type"], reverse=True)
        elif task["type"] == "heading":
            heading = task
            heading["items"] = tasks(
                type="to-do",
                heading=heading["uuid"],
                context_trashed=None,
                include_items=True,
                database=database,
            )

    if uuid:
        result = result[0]

    return result


def areas(uuid=None, include_items=False, **kwargs):
    """
    Read areas into dicts.

    Parameters
    ----------
    uuid : str or None, optional
        Any valid uuid of an area. If None, then return all areas.

    include_items : bool, default False
        Include tasks and projects in each area.

    tag : str or bool or None, optional
        Any valid title of a tag. Only include areas matching that tag.
        Special cases:
        - `tag == False`, only include areas _without_ tags.
        - `tag == True`, only include areas _with_ tags.
        - `tag == None`, then ignore any tags present, that is,
           include areas both with and without tags.

    count_only : bool, default False
        Only output length of result. This is done by a SQL COUNT query.

    filepath : str, optional
        Any valid path of a SQLite database file generated by the Things app.
        If no path is provided, then access the default database path.

    database : things.database.Database, optional
        Any valid `things.database.Database` object previously instantiated.

    Returns
    -------
    list of dict (default)
        Representing Things areas.
    dict (if `uuid` is given)
        Representing a single Things area.
    int (`count_only == True`)
        Count of matching areas.

    Examples
    --------
    >>> things.areas()
    [{'uuid': 'Y3JC4XeyGWxzDocQL4aobo', 'type': 'area', 'title': 'Area 3'}, ...
    >>> things.areas(tag='Home')
    []
    >>> things.areas(uuid='DciSFacytdrNG1nRaMJPgY')
    {'uuid': 'DciSFacytdrNG1nRaMJPgY', 'type': 'area', 'title': 'Area 1', ...
    >>> things.areas(include_items=True, tag='Errand')
    [{'uuid': 'DciSFacytdrNG1nRaMJPgY', 'type': 'area', 'title': 'Area 1', ...
    """
    database = pop_database(kwargs)
    result = database.get_areas(uuid=uuid, **kwargs)

    if kwargs.get("count_only"):
        return result

    for area in result:
        if area.get("tags"):
            area["tags"] = database.get_tags(area=area["uuid"])
        if include_items:
            area["items"] = tasks(
                area=area["uuid"], include_items=True, database=database
            )

    if uuid:
        result = result[0]

    return result


def tags(title=None, include_items=False, **kwargs):
    """
    Read tags into dicts.

    Parameters
    ----------
    title : str, optional
        Any valid title of a tag. Include all items of said tag.
        If None, then return all tags.

    include_items : bool, default False
        For each tag, include items tagged with that tag.
        Items may include areas, tasks, and projects.

    area : str, optional
        Valid uuid of an area. Return tags of said area.

    task : str, optional
        Valid uuid of a task. Return tags of said task.

    titles_only : bool, default False
        If True, only return list of titles of tags.

    filepath : str, optional
        Any valid path of a SQLite database file generated by the Things app.
        If no path is provided, then access the default database path.

    database : things.database.Database, optional
        Any valid database object previously instantiated.

    Returns
    -------
    list of dict (default)
        Representing tags.
    list of str (if `titles_only == True` or area / task is given)
        Representing tag titles.
    dict (if `title` is given)
        Representing a single Things tag.

    Examples
    --------
    >>> things.tags()
    [{'uuid': 'H96sVJwE7VJveAnv7itmux', 'type': 'tag', 'title': 'Errand', ...
    >>> things.tags('Home')
    {'uuid': 'CK9dARrf2ezbFvrVUUxkHE', 'type': 'tag', 'title': 'Home', ...
    >>> things.tags(include_items=True)
    [{'uuid': 'H96sVJwE7VJveAnv7itmux', 'type': 'tag', 'title': 'Errand', ...
    >>> things.tags(task='2Ukg8I2nLukhyEM7wYiBeb')
    []
    """
    database = pop_database(kwargs)
    result = database.get_tags(title=title, **kwargs)

    if include_items:
        for tag in result:
            tag_title = tag["title"]
            tag["items"] = [
                *areas(tag=tag_title, database=database),
                *tasks(tag=tag_title, database=database),
            ]

    if title:
        result = result[0]

    return result


def checklist_items(todo_uuid, **kwargs):
    """
    Read checklist items of to-dos into dicts.

    Note: checklists are contained in the return value of
    `things.todos(todo_uuid)` and `things.tasks(todo_uuid)`.

    Parameters
    ----------
    todo_uuid : str, optional
        A valid to-do uuid.

    Returns
    -------
    list of dict
        Checklist items.
    """
    database = pop_database(kwargs)
    return database.get_checklist_items(todo_uuid=todo_uuid)


# --------------------------------------------------
# Utility API functions derived from above
# --------------------------------------------------


def search(query: str, **kwargs) -> List[Dict]:
    """
    Search tasks in the database.

    Currently any part of a title and note of a to-do, project,
    heading, or area is matched.

    See the `search_query` parameter of `things.api.tasks` for details.

    Examples
    --------
    >>> things.search('Today%yellow')
    [{'uuid': '6Hf2qWBjWhq7B1xszwdo34',
      'type': 'to-do',
      'title': 'Upcoming To-Do in Today (yellow)',
      'status': 'incomplete',
      'notes': '',
      ...
    """
    return tasks(search_query=query, **kwargs)


def get(uuid, default=None, **kwargs):
    """
    Find an object by uuid. If not found, return `default`.

    Currently supports tasks, projects, headings, areas, and tags.
    """
    try:
        return tasks(uuid=uuid, **kwargs)
    except ValueError:
        pass

    try:
        return areas(uuid=uuid, **kwargs)
    except ValueError:
        pass

    for tag in tags(**kwargs):
        if tag["uuid"] == uuid:
            return tag

    return default


# Filter by object type


def todos(uuid=None, **kwargs):
    """
    Read to-dos into dicts.

    See `things.api.tasks` for details on the optional parameters.
    """
    return tasks(uuid=uuid, type="to-do", **kwargs)


def projects(uuid=None, **kwargs):
    """
    Read projects into dicts.

    See `things.api.tasks` for details on the optional parameters.
    """
    return tasks(uuid=uuid, type="project", **kwargs)


# Filter by collections in the Things app sidebar.


def inbox(**kwargs):
    """
    Read Inbox into dicts.

    See `things.api.tasks` for details on the optional parameters.
    """
    return tasks(start="Inbox", **kwargs)


def today(**kwargs):
    """
    Read Today's tasks into dicts.

    Note: The Things database reflects the state of the Things app when
    it was last opened. For the Today tasks that means the database
    might not be up to date anymore if you didn't open the app recently.
    To get around this limitation, we here make a prediction of what
    tasks would show up in Today if you were to open the app right now.
    This prediction does not include repeating tasks at this time.

    See `things.api.tasks` for details on the optional parameters.
    """
    database = pop_database(kwargs)
    kwargs["database"] = database

    regular_today_tasks = tasks(
        start_date=True,
        start="Anytime",
        index="todayIndex",
        **kwargs,
    )

    # Predictions of new to-dos indicated by a yellow dot in the app.

    unconfirmed_scheduled_tasks = tasks(
        start_date="past",
        start="Someday",
        index="todayIndex",
        **kwargs,
    )

    unconfirmed_overdue_tasks = tasks(
        start_date=False,
        deadline="past",
        deadline_suppressed=False,
        **kwargs,
    )

    result = [
        *regular_today_tasks,
        *unconfirmed_scheduled_tasks,
        *unconfirmed_overdue_tasks,
    ]
    result.sort(key=lambda task: (task["today_index"], task["start_date"]))

    return result


def upcoming(**kwargs):
    """
    Read Upcoming tasks into dicts.

    Note: unscheduled tasks with a deadline are not included here.
    See the `things.api.deadline` function instead.

    For details on parameters, see `things.api.tasks`.
    """
    return tasks(start_date="future", start="Someday", **kwargs)


def anytime(**kwargs):
    """
    Read Anytime tasks into dicts.

    See `things.api.tasks` for details on the optional parameters.
    """
    return tasks(start="Anytime", **kwargs)


def someday(**kwargs):
    """
    Read Someday tasks into dicts.

    See `things.api.tasks` for details on the optional parameters.
    """
    return tasks(start_date=False, start="Someday", **kwargs)


def logbook(**kwargs):
    """
    Read Logbook tasks into dicts.

    See `things.api.tasks` for details on the optional parameters.
    """
    result = [*canceled(**kwargs), *completed(**kwargs)]
    result.sort(key=lambda task: task["stop_date"], reverse=True)
    return result


def trash(**kwargs):
    """
    Read Trash tasks into dicts.

    See `things.api.tasks` for details on the optional parameters.
    """
    return tasks(
        trashed=True,
        context_trashed=kwargs.pop("context_trashed", None),
        status=kwargs.pop("status", None),
        **kwargs,
    )


# Filter by various task properties


def canceled(**kwargs):
    """
    Read canceled tasks into dicts.

    See `things.api.tasks` for details on the optional parameters.
    """
    return tasks(status="canceled", **kwargs)


def completed(**kwargs):
    """
    Read completed tasks into dicts.

    See `things.api.tasks` for details on the optional parameters.

    Examples
    --------
    >>> things.completed(count_only=True)
    10
    >>> things.completed(type='project', count_only=True)
    0
    >>> things.completed(type='to-do', last='1w')
    []
    """
    return tasks(status="completed", **kwargs)


def deadlines(**kwargs):
    """
    Read tasks with deadlines into dicts.

    See `things.api.tasks` for details on the optional parameters.
    """
    result = tasks(deadline=True, **kwargs)
    result.sort(key=lambda task: task["deadline"])
    return result


def last(offset, **kwargs):
    """
    Read tasks created within last X days, weeks, or years into dicts.

    Per default, only incomplete tasks are included, but do see
    `things.api.tasks` for details on the optional parameters.

    Parameters
    ----------
    offset : str
        A valid date offset such as '3d', '5w', or '1y'.
        For details, see the `last` parameter of `things.api.tasks`.

    Returns
    -------
    list of dict
        Tasks within offset ordered by creation date. Newest first.

    Examples
    --------
    >>> things.last('3d')
    []
    >>> things.last('1w', status='completed')
    []
    >>> things.last('1y', tag='Important', status='completed', count_only=True)
    0

    """
    if offset is None:
        raise ValueError(f"Invalid offset type: {offset!r}")

    result = tasks(last=offset, **kwargs)
    if result:
        result.sort(key=lambda task: task["created"], reverse=True)

    return result


# Interact with Things app


def token(**kwargs) -> Union[str, None]:
    """
    Read the Things URL scheme authentication token.

    You can make good use of this token to modify existing Things data
    using the Things URL Scheme. For details, see
    [here](https://culturedcode.com/things/help/url-scheme/).
    """
    database = pop_database(kwargs)
    return database.get_url_scheme_auth_token()


def link(uuid):
    """Return a things:///show?id=uuid link."""
    return f"things:///show?id={uuid}"


def show(uuid):  # noqa
    """
    Show a certain uuid in the Things app.

    Parameters
    ----------
    uuid : str
        A valid uuid of any Things object.

    Examples
    --------
    >>> tag = things.tags('Home')
    >>> things.show(tag['uuid'])  # doctest: +SKIP
    """
    uri = link(uuid)
    os.system(f"open {quote(uri)}")


# Helper functions


def pop_database(kwargs):
    """Instantiate non-default database from `kwargs` if provided."""
    filepath = kwargs.pop("filepath", None)
    database = kwargs.pop("database", None)
    print_sql = kwargs.pop("print_sql", False)

    if not database:
        database = Database(filepath=filepath, print_sql=print_sql)
    return database
