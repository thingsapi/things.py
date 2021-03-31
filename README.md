# Things Python API

A simple Python 3 library to read your [Things app](https://culturedcode.com/things) data. You can test the API [via our CLI](https://github.com/thingsapi/things-cli).

[![Build Status](https://github.com/thingsapi/things.py/workflows/Build-Test/badge.svg)](https://github.com/thingsapi/things.py/actions)
[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/quality/g/thingsapi/things.py)](https://scrutinizer-ci.com/g/thingsapi/things.py/?branch=master)
[![Coverage Status](https://codecov.io/gh/thingsapi/things.py/branch/main/graph/badge.svg?token=DBWGKAEYAP)](https://codecov.io/gh/thingsapi/things.py)
[![GitHub Issues](https://img.shields.io/github/issues/thingsapi/things.py)](https://github.com/thingsapi/things.py/issues)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![GitHub Release](https://img.shields.io/github/v/release/thingsapi/things.py?sort=semver)](https://github.com/thingsapi/things.py/releases)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/things.py?label=pypi%20downloads)](https://pypi.org/project/things.py/)
[![GitHub Download Count](https://img.shields.io/github/downloads/thingsapi/things.py/total.svg)](https://github.com/thingsapi/things.py/releases)

## Table of Contents

- [Install](#install)
- [Examples](#examples)
- [Background](#background)
- [Things URLs](#things-urls)

## Install

```sh
$ pip3 install things.py
# or
$ git clone https://github.com/thingsapi/things.py && cd things.py && make install
```

## Examples

```python
>>> import things
>>> things.todos()
[{'uuid': '2Ukg8I2nLukhyEM7wYiBeb',
  'type': 'to-do',
  'title': 'Make reservation for dinner',
  'project': 'bNj6TPdKYhY6fScvXWVRDX',
  ...},
 {'uuid': 'RLZroza3jz0XPs3uAlynS7',
  'type': 'to-do',
  'title': 'Buy a whiteboard and accessories',
  'project': 'w8oSP1HjWstPin8RMaJOtB',
  'notes': "Something around 4' x 3' that's free-standing, two-sided, and magnetic.",
  'checklist': True,
  ...
>>> things.todos('RLZroza3jz0XPs3uAlynS7')
{'uuid': 'RLZroza3jz0XPs3uAlynS7',
 'type': 'to-do',
 'title': 'Buy a whiteboard and accessories',
 ...
 'checklist': [
     {'title': 'Cleaning Spray', 'status': 'completed', ...},
     {'title': 'Magnetic Eraser', 'status': 'incomplete', ...},
     {'title': 'Round magnets', 'status': 'incomplete', ...}
 ]
 ...
}

>>> things.projects()
[{'uuid': 'bNj6TPdKYhY6fScvXWVRDX',
  'type': 'project',
  'title': 'Throw Birthday Party',
  'area': 'bNj6TPdKYhY6fScvXWVRDX',
  ...},
 {'uuid': 'w8oSP1HjWstPin8RMaJOtB',
  'type': 'project',
  'title': 'Set Up Home Office',
  'area': 'Gw9QefIdgR6nPEoY5hBNSh',
  ...

>>> things.areas()
[{'uuid': 'ToLxnnBrWkfHC3tkx4vxdV',
  'type': 'area',
  'title': 'Family',
  ...},
 {'uuid': 'Gw9QefIdgR6nPEoY5hBNSh',
  'type': 'area',
  'title': 'Apartment',
  ...

>>> things.tags()
[{'uuid': 'CKILg3kKF2jlCRisNFcqOj',
  'type': 'tag',
  'title': 'Home',
  'shortcut': None},
 {'uuid': 'gfmpz8zxnyfqMDvRi3E8vo',
  'type': 'tag',
  'title': 'Office',
  'shortcut': None},
 ...

>>> things.get('CKILg3kKF2jlCRisNFcqOj')
{'uuid': 'CKILg3kKF2jlCRisNFcqOj',
  'type': 'tag',
  'title': 'Home',
  'shortcut': None}

```

## Background

The task management app Things stores all your to-dos in a SQLite database file (details [here](https://culturedcode.com/things/support/articles/2982272/#get-the-things-3-database-file)). This format is machine-readable, not human-readable. The aim of this project is let you access all your data in a human-readable way. We thereby stay as true to the database as possible while doing SQL Joins and transformations to aid understanding of the data.

Here's the terminology used involving the database:

- area
- tag
- task
  - type
    - `'to-do'`: may have a checklist; may be in an area and have tags.
    - `'project'`: may have to-dos and headings; may be in an area and have tags.
    - `'heading'`:  part of a project; groups "tasks".
  - status:  `"incomplete"`,  `"canceled"`, or `"completed"`
  - trashed: `True` or `False`
  - start: `"Inbox"`, `"Anytime"`, or `"Someday"`
- checklist item (contained within a to-do)

## Things URLs

You can make good use of the `uuid` to link to to-dos, areas, tags, and more from other apps. Read more [here](https://culturedcode.com/things/blog/2018/02/hey-things/).
