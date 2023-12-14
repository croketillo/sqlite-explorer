import sqlite3
import sys
sys.path.append('src')
from functions import get_table_schema_data, get_all_table_data, print_table_data

# Name of the test database
TEST_DB = "test_database.db"

def create_test_database():
    # Delete the database if it already exists
    try:
        connection = sqlite3.connect(TEST_DB)
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS test_table;")
        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        print(f"Error deleting the database: {e}")

    # Create the test database
    try:
        connection = sqlite3.connect(TEST_DB)
        cursor = connection.cursor()

        # Create a test table and add some data
        cursor.execute("""
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            );
        """)

        # Insert some data
        data_to_insert = [
            (1, 'John', 25),
            (2, 'Jane', 30),
            (3, 'Bob', 35),
            (4, 'Alice', 28),
            (5, 'Charlie', 40),
            (6, 'Eve', 22),
            (7, 'David', 33),
            (8, 'Grace', 31),
            (9, 'Frank', 36),
            (10, 'Helen', 27)
        ]

        cursor.executemany("INSERT INTO test_table (id, name, age) VALUES (?, ?, ?);", data_to_insert)

        # Save changes and close the connection
        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        print(f"Error creating the test database: {e}")

# Call the function to create the test database
create_test_database()

def test_get_table_schema_data():
    connection = sqlite3.connect(TEST_DB)
    rows, _ = get_table_schema_data(connection, "test_table")  # Unpack only rows, you don't need entry_count
    connection.close()

    # Actual structure of the test_table
    expected_rows = [
        ('id', 'INTEGER', 'NO', 'YES'),
        ('name', 'TEXT', 'NO', 'NO'),
        ('age', 'INTEGER', 'NO', 'NO')
    ]

    for expected, actual in zip(expected_rows, rows):
        assert expected[0] == actual[0]  # Compare column names
        assert expected[1] == actual[1]  # Compare data types
        assert expected[3] == actual[3]  # Compare primary keys

def test_print_table_data(capsys):
    connection = sqlite3.connect(TEST_DB)
    data, column_names = get_all_table_data(connection, "test_table")
    print_table_data(data, "test_table", column_names)

    # Define expected values
    expected_data = [
        (1, 'John', 25),
        (2, 'Jane', 30),
        (3, 'Bob', 35),
        (4, 'Alice', 28),
        (5, 'Charlie', 40),
        (6, 'Eve', 22),
        (7, 'David', 33),
        (8, 'Grace', 31),
        (9, 'Frank', 36),
        (10, 'Helen', 27)
    ]

    # Verify that the retrieved data matches the expected values
    assert data == expected_data

import textwrap

def test_get_all_table_data():
    connection = sqlite3.connect(TEST_DB)
    data, column_names = get_all_table_data(connection, "test_table")
    connection.close()

    # Ensure the correct number of rows
    assert len(data) == 10
    
    # Get expected column names
    expected_column_names = ['id', 'name', 'age']
    
    # Ensure column names are correct
    expected_output = textwrap.dedent(f"""
        {expected_column_names}
    """)

    assert column_names == expected_column_names
