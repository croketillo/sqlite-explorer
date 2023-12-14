import sqlite3
import click
from colorama import Fore, Style
from sqlite_explorer.functions import (
    get_table_schema_data,
    print_table_schema,
    print_table_data
)

@click.group()
def cli():
    pass

@cli.command()
@click.argument('database')
def schemas(database):
    """Print schema for all tables in the database."""
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        rows, entry_count = get_table_schema_data(connection, table_name)
        print_table_schema(rows, table_name, entry_count)

    connection.close()

@cli.command()
@click.argument('database')
@click.argument('table_name')
def table(database, table_name):
    """Print schema for a specific table."""
    connection = sqlite3.connect(database)
    rows, entry_count = get_table_schema_data(connection, table_name)
    print_table_schema(rows, table_name, entry_count)
    connection.close()

@cli.command()
@click.argument('database')
def list_tables(database):
    """List all tables in the database."""
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print(f"\n{Fore.CYAN}{Style.BRIGHT}TABLES IN DATABASE: {database}{Style.RESET_ALL}\n")
    for table in tables:
        print(table[0])

    connection.close()

@cli.command()
@click.argument('database')
@click.argument('table_name')
def list_columns(database, table_name):
    """List columns for a specific table."""
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    print(f"\n{Fore.CYAN}{Style.BRIGHT}COLUMNS IN TABLE: {table_name}{Style.RESET_ALL}\n")

    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()

    for column in columns:
        print(column[1])

    connection.close()

@cli.command()
@click.argument('database')
@click.argument('sql_statement')
def exec(database, sql_statement):
    """Execute a SQL statement in the database."""
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    try:
        cursor.execute(sql_statement)
        connection.commit()
        print(f"\n{Fore.GREEN}{Style.BRIGHT}SQL statement executed successfully.{Style.RESET_ALL}\n")

    except sqlite3.Error as e:
        print(f"\n{Fore.RED}{Style.BRIGHT}Error executing SQL statement:{Style.RESET_ALL} {e}\n")

    finally:
        connection.close()

@cli.command()
@click.argument('database')
@click.argument('table_name')
@click.option('--limit', default=None, help='Number of results to show. Use a positive value for the first results and a negative value for the last results.')
def data(database, table_name, limit):
    """Retrieve and print data for a specific table."""
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    # Get column names
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]

    # Form the final query
    query = f"SELECT {', '.join(column_names)} FROM {table_name};"

    # Execute the query
    cursor.execute(query)
    data = cursor.fetchall()

    if limit is not None:
        limit = int(limit)
        data = data[:limit] if limit > 0 else data[limit:]

    print_table_data(data, table_name, column_names)
    connection.close()


if __name__ == '__main__':
    cli()
