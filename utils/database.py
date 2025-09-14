import sqlite3

def initialize_database(db_name: str = 'meals_database.db') -> None:
    """Initialize the SQLite database and create the meals table if it doesn't exist.
    Args:
        db_name (str): The name of the SQLite database file.
    """
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY,
                meal_name TEXT NOT NULL,
                grocery_items TEXT,
                able_to_make_more_for_lunch BOOLEAN,
                cuisine TEXT
            )
        ''')
        conn.commit()

def execute_query_on_database(sql_query: str, sql_query_args: list, db_name: str = 'meals_database.db') -> list:
    """Connect to the SQLite database and execute a query.
    Args:
        sql_query (str): The SQL query to execute.
        sql_query_args (list): The arguments for the SQL query.
        db_name (str): The name of the SQLite database file.
    Returns:
        list: The result of the query as a list of tuples.
    """

    initialize_database(db_name)  # Ensure the database and table are initialized
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(sql_query, sql_query_args)
        return cursor.fetchall()

def cleanup_database(db_name: str = 'meals_database.db') -> None:
    """Clean up the database by removing all records from the meals table.
    Args:
        db_name (str): The name of the SQLite database file.
    """
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM meals')
        conn.commit()

def get_all_meal_records_from_db(db_name: str = 'meals_database.db') -> list:
    """Fetch all meal records from the database.
    Args:
        db_name (str): The name of the SQLite database file.
    Returns:
        list: A list of meal records, where each record is a tuple containing meal details:
        (id, meal_name, grocery_items, able_to_make_more_for_lunch, cuisine).
    """
    initialize_database(db_name)  # Ensure the database and table are initialized

    # Using a context manager to ensure the connection is closed properly
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM meals')
        meal_records = cursor.fetchall()
    return meal_records

def add_meal_to_db(meal_name: str, grocery_items: str, able_to_make_more_for_lunch: bool, cuisine: str, db_name: str = 'meals_database.db') -> None:
    """Add a new meal to the database.
    Args:
        meal_name (str): The name of the meal.
        grocery_items (str): Comma-separated list of grocery items.
        able_to_make_more_for_lunch (bool): Whether more can be made for lunch.
        cuisine (str): The type of cuisine.
        db_name (str): The name of the SQLite database file.
    """
    initialize_database(db_name)  # Ensure the database and table are initialized

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO meals (meal_name, grocery_items, able_to_make_more_for_lunch, cuisine)
            VALUES (?, ?, ?, ?)
        ''', (meal_name, grocery_items, able_to_make_more_for_lunch, cuisine))
        conn.commit()

# Example usage
if __name__ == "__main__":

    # Add a new meal to the database
    # add_meal_to_db(
    #     meal_name="Pasta Primavera",
    #     grocery_items="Pasta, Vegetables, Olive Oil, Garlic",
    #     able_to_make_more_for_lunch=True,
    #     cuisine="Italian"
    # )

    # Example of executing a custom query
    # execute_query_on_database(
    #     sql_query="UPDATE meals SET able_to_make_more_for_lunch = ? WHERE meal_name = ?",
    #     sql_query_args=[False, "Pasta Primavera"]
    # )
    # result = execute_query_on_database(
    #     sql_query="SELECT * FROM meals WHERE cuisine = ?",
    #     sql_query_args=["Italian"]
    # )
    # print("Query result:", result)

    # Fetch all meal records again to see the update
    meals = get_all_meal_records_from_db()

    print("All meal records:", meals)
    meal_names = [meal[1] for meal in meals]  # Extracting meal names from the records
    print("Available meal names:", meal_names)

