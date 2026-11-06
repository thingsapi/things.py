# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-10

### Added

- `make update` target to update dependencies via `pipenv update --dev` and `npm update pyright`
- `complete()` function to mark tasks as complete programmatically (#121)
  - Accepts a task UUID and marks the task as complete
  - Returns the updated task object
- `url()` function as the main way to generate Things URLs (#121)
  - Replaces the previous `link()` function
  - Includes proper URL encoding for query parameters
  - `link()` remains as a backwards-compatible alias
- `reminder_time` field in task output (#133)
  - Available in `tasks()` and related API endpoints
  - Returns the reminder time if set for a to-do
- `CONTRIBUTING.md` with contribution guidelines (#123)
  - Instructions for setting up development environment
  - Guidelines for submitting pull requests
  - Test database setup instructions
- "Used by Things Review" to README (#116)

### Changed

- Invoke pylint via pipenv to use compatible version (fixes Python 3.13 compatibility)
- Copyright year updated to 2026
- Database connection handling (#125, #126, #132)
  - Database now closes connection when garbage collected via weakref finalize (#132)
  - Database now uses a single connection for all queries (#126)
  - Previously leaked connections due to lack of cleanup
  - Reduces connection overhead and fixes errors with large todo lists (~2500 items)

### Fixed

- Lint fixes for pycodestyle, pydocstyle, and pylint
- `stop_date` where clause now uses `localtime` for accurate date filtering (#117, #118)
- Static code analyzer support with `assert_never` in database.py (#121)
- Timezone handling improvements
  - Added `tzset()` for non-macOS platforms
  - Additional timezone tests across UTC
- CONTRIBUTING.md link in README pointing to master instead of main (#124)
- Various import and linting issues

### Documentation

- Extended "Used By" section in README with more projects
- Added timezone variable setting documentation
- Updated test documentation for testdoc failures
- Various README updates

### Contributors

- @mbhutton (#125, #126, #132)
- @HiJohnElliott (#133)
- @cato447 (#121)
- @chrisgurney (#117, #118, #123, #124)
- @minthemiddle (#116)

## [Unreleased]

## [1.1.0] - 2026-10-26

### Changed

- Require Python 3.11 as minimum version (dropped 3.8-3.10, CI tests 3.11+) (#151)
- Rework how the Things database location is determined (#149)
  - Permission errors for the Things app Group Container are now surfaced instead of silently falling back
  - Setting `THINGSDB` (or passing `filepath` to `Database()`) never looks into the Group Container anymore
  - `things.database.DEFAULT_FILEPATH` was removed, use `things.database.get_default_database_filepath()` instead
  - Default path constant renamed for the Things 3.17.4 data folder; obsolete database-move migration code removed
- Consolidate packaging and lint config in `pyproject.toml` (`setup.py`, `setup.cfg`, `ruff.toml`, empty `requirements.txt` and `.pylintrc` removed; flake8/pycodestyle/pydocstyle/isort checks now handled by ruff) (#151)

## [1.0.1] - 2026-02-28

### Fixed

- `today()` no longer crashes on tasks without a start date
- Deploy workflow installs `setuptools` so the build works

## [0.0.15] - 2023-05-22

### Added

- New database support for Things 3.15.16+ (#107, #105, #100)
  - New database path
  - New date format
  - New column names

### Changed

- New options for `start_date`, `stop_date`, and `deadline` parameters
- Added more typing, modernized codebase, fixed tests (#104)

### Fixed

- Return tagged items that are assigned to a heading (#94)
- Various import and linting issues

### Documentation

- Various README updates

### Contributors

- @CaAlden (#103)
- @bkleinen (#96)
- @fabge (#106)

## [0.0.14] - 2021-12-13

### Fixed

- #93: `start_date` and `deadline` are off by one day

## [0.0.13] - 2021-11-14

### Added

- Support for a specific `stop_date` (e.g., used to show logged items today)

## [0.0.12] - 2021-06-06

### Added

- `context_trashed` parameter

### Fixed

- `things.trash` to include items
- Show "yellow" tasks in Today

### Changed

- Refactored `get_task_by_uuid` out of `get_tasks` in `database.Database` to decrease code complexity
- Updated documentation and SQL date filters in `database`

## [0.0.11] - 2021-04-19

## [0.0.10] - 2021-04-13

### Documentation

- Updated docs

## [0.0.9] - 2021-04-12

## [0.0.8] - 2021-04-12

## [0.0.7] - 2021-04-08

### Documentation

- Updated docs

## [0.0.6] - 2021-04-05

## [0.0.5] - 2021-04-04

## [0.0.4] - 2021-04-01

## [0.0.3] - 2021-03-31

## [0.0.2] - 2021-03-30

### Added

- Initial release

[Unreleased]: https://github.com/thingsapi/things.py/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/thingsapi/things.py/releases/tag/v1.1.0
[1.0.1]: https://github.com/thingsapi/things.py/releases/tag/v1.0.1
[1.0.0]: https://github.com/thingsapi/things.py/releases/tag/v1.0.0
[0.0.15]: https://github.com/thingsapi/things.py/releases/tag/v0.0.15
[0.0.14]: https://github.com/thingsapi/things.py/releases/tag/v0.0.14
[0.0.13]: https://github.com/thingsapi/things.py/releases/tag/v0.0.13
[0.0.12]: https://github.com/thingsapi/things.py/releases/tag/v0.0.12
