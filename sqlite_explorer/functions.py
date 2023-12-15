from tabulate import tabulate
from colorama import Fore, Style
import sqlite3
import csv

def get_table_schema_data(connection, table_name):
    """
    Retrieve schema data for a specific table.

    Parameters:
    - connection (sqlite3.Connection): The SQLite database connection.
    - table_name (str): The name of the table.

    Returns:
    Tuple: A tuple containing the list of rows (schema) and the number of entries.
    """
    cursor = connection.cursor()

    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()

    rows = []
    for column in columns:
        column_name = column[1]
        data_type = column[2]
        allows_null = "NO" if column[3] == 0 else "YES"
        primary_key = "YES" if column[5] == 1 else "NO"

        row = [column_name, data_type, allows_null, primary_key]
        rows.append(row)

    # Get the number of entries in the table
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    entry_count = cursor.fetchone()[0]

    return rows, entry_count

def print_table_schema(rows, table_name, entry_count):
    """
    Print the schema for a specific table.

    Parameters:
    - rows (list): List of rows (schema data).
    - table_name (str): The name of the table.
    - entry_count (int): The number of entries in the table.

    Returns:
    None
    """
    print(f"\n{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}SCHEMA FOR TABLE:{Fore.BLUE}{Style.NORMAL} {table_name}{Style.RESET_ALL}\n")

    headers = ["Column Name", "Data Type", "Allows Null", "Primary Key"]
    print(tabulate(rows, headers, tablefmt="grid"))

    print(f"Number of Entries: {entry_count}\n")

def get_all_table_data(connection, table_name):
    """
    Retrieve all data for a specific table.

    Parameters:
    - connection (sqlite3.Connection): The SQLite database connection.
    - table_name (str): The name of the table.

    Returns:
    List: A list containing all rows of data from the table.
    """
    cursor = connection.cursor()
    
    # Get column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    column_info = cursor.fetchall()
    column_names = [column[1] for column in column_info]

    # Get all data from the table
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()

    return data, column_names

def print_table_data(data, table_name, column_names):
    """
    Print data for a specific table.

    Parameters:
    - data (list): List of rows (table data), can be a list of dictionaries or tuples.
    - table_name (str): The name of the table.

    Returns:
    None
    """
    if not data:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}No data found for table:{Fore.BLUE}{Style.NORMAL} {table_name}{Style.RESET_ALL}\n")
        return

    if isinstance(data[0], dict):
        headers = [key for key in data[0].keys()]
    elif isinstance(data[0], tuple):
        headers = column_names
    else:
        raise ValueError("Unsupported data format. Use a list of dictionaries or tuples.")

    print(f"\n{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}DATA FOR TABLE:{Fore.BLUE}{Style.NORMAL} {table_name}{Style.RESET_ALL}\n")
    print(tabulate(data, headers, tablefmt="grid"))
