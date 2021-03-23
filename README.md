Get your Things app data into a Python dict.

## Install
```python
$ pip install things.py
```

## Run
```pycon
>>> import things
>>> things.tasks()
[{'uuid': '2Ukg8I2nLukhyEM7wYiBeb',
  'type': 'task',
  'title': 'Make reservation for dinner',
  'project': {'title': 'Throw Birthday Party', 'uuid': 'bNj6TPdKYhY6fScvXWVRDX'},
  ...},
 {'uuid': 'RLZroza3jz0XPs3uAlynS7',
  'type': 'task',
  'title': 'Buy a whiteboard and accessories',
  'project': {'title': 'Set Up Home Office', 'uuid': 'w8oSP1HjWstPin8RMaJOtB'},
  'notes': "Something around 4' x 3' that's free-standing, two-sided, and magnetic.',
  'tags': [],
  'checklist': [
      {'title': 'Cleaning Spray', 'status': 'done', ...},
      {'title': 'Magnetic Eraser', 'status': 'open', ...},
      {'title': 'Round magnets', 'status': 'open', ...}
  ],
  ...

>>> things.areas()
[{'uuid': 'hIo1FJlAYGKt1Yj38vzKc3',
  'type': 'area',
  'title': 'Family',
  'tasks': [],
  'projects': [
    {'uuid': '2Ukg8I2nLukhyEM7wYiBeb',
     'type': 'project',
     'title': 'Vacation in Rome',
     'tasks': [
       {'uuid': 'jqBQAmQJOdnqVJRCuwaXcU',
        'type': 'task',
        'title': "Borrow Sarah's travel guide",
        ...}],
     'headings': [
       {'uuid': 'gln1iLefjDXKkKIQLTqiWE',
        'type': 'heading',
        'title': 'Pack',
        'tasks': [...]
        ...},
 ...

>>> things.tags()
[{'uuid': 'hIo1FJlAYGKt1Yj38vzKc3',
  'type': 'tag',
  'title': 'Home',
  'shortcut': None},
 {'uuid': 'hIo1FJlAYGKt1Yj38vzKc3',
  'type': 'tag',
  'title': 'Office',
  'shortcut': None},
 ...

>>> things.get('hIo1FJlAYGKt1Yj38vzKc3')
{'uuid': 'hIo1FJlAYGKt1Yj38vzKc3',
  'type': 'tag',
  'title': 'Home',
  'shortcut': None}
```

>>> things.get_all()
{
  'areas': [...],     # areas include contained projects and tasks
  'projects': [...],  # projects not contained in any area
  'tasks': [...],     # tasks not contained in any project or area
  'tags': [...]
}


## Technical Background

The task management app Things stores all your to-dos in a SQLite database file (details [here](https://culturedcode.com/things/support/articles/2982272/#get-the-things-3-database-file)). This format is machine-readable, not human-readable. The aim of this project is let you access all your data in a human-readable way. We thereby stay as true to the database as possible while doing SQL Joins and transformations to aid understanding of the data.

Here's the terminology used involving the database:

- Area
- Tag
- Task
  - type
    - `"task"`: task within a project or a standalone task; can link to an area, tags, and a checklist
    - `"project"`: a supertask; can link to an area, tags, (sub)tasks, and headings.
    - `"heading"`: contained within a project in order to group tasks
  - status:  `"open"`,  `"cancelled"`, or `"done"`
  - trashed: `True` or `False`
- Checklist Item (contained within a task)

## Things URLs

You can make good use of the `uuid` to link to tasks, areas, tags, and more from other apps. Read more [here](https://culturedcode.com/things/blog/2018/02/hey-things/).
