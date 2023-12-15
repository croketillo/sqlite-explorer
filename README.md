# SQLiteExplorer

SQLiteExplorer is a command-line application designed for the manipulation of SQLite databases. With SQLiteExplorer, you can easily visualize table schemas, execute SQL queries, manage data within tables, and list tables and columns. It provides a convenient and efficient way to interact with SQLite databases directly from the command line.

## Features
- Visualization of table schemas.
- Execution of SQL queries.
- Data management in tables.
- Listing of tables and columns.
- Export to csv files. (Version 0.1.2)

## Quick Start

### Install

```bash
pip install sqlite-explorer
```

### Usage

```bash
sqlexp --help
```

```
Usage: sqlexp [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  data          Retrieve and print data for a specific table.
  exec          Execute a SQL statement in the database.
  list-columns  List columns for a specific table.
  list-tables   List all tables in the database.
  schemas       Print schema for all tables in the database.
  table         Print schema for a specific table.
```

## License

This project is licensed under the GNU-GPL License. See the LICENSE file for more details.
