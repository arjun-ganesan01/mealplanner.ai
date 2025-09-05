from mcp.server.fastmcp import FastMCP
import database
import json

# Create an MCP server instance
mcp = FastMCP("Meal Planner Service")

DB_NAME = 'meals_database.db'

@mcp.tool("read_all_meal_records_from_db")
# Passing complex data structures like lists of tuples directly to MCP tools can sometimes lead to serialization issues.
# To avoid this, we serialize the list of tuples to a JSON string before returning it.
def read_all_meal_records_from_db() -> str:
    """This tool fetches all meal records from the database.
    This is useful for viewing all meals stored in the database.
    It returns a list of tuples containing meal records, where each record is a tuple containing meal details.
    If the user wants to see all meals, they can use this tool.
    Args:
        None
    Returns:
        str:
          Returns a JSON-encoded list of meal records.
          In the list of meal records, each record is a tuple containing meal details.
          Tuple format: (id, meal_name, grocery_items, able_to_make_more_for_lunch, cuisine).
    """
    return_val = (database.get_all_meal_records_from_db(DB_NAME))
    return json.dumps(return_val)

@mcp.tool("get_all_meal_names_from_db")
def get_all_meal_names_from_db() -> str:
    """This tool fetches all meal names from the database.
    This is useful for viewing all meal names stored in the database.
    It returns a list of meal names as strings.
    If the user wants to see all meal names, they can use this tool.
    Args:
        None
    Returns:
        str: A comma-separated string of all meal names in the database.
    """

    meals = database.get_all_meal_records_from_db()

    # Extract meal names from the records                                                                                                                            
    meal_names = [meal[1] for meal in meals]

    combined_meal_names = ", ".join(meal_names)
    return combined_meal_names

@mcp.tool("add_meal_to_db")
def add_meal_to_db(meal_name: str, grocery_items: str, able_to_make_more_for_lunch: bool, cuisine: str) -> str:
    """This tool adds a new meal to the database.
    It is useful for adding meals that are not already in the database.
    The meal name, grocery items, and cuisine must be provided.
    The `able_to_make_more_for_lunch` parameter indicates whether more can be made for lunch.
    If the user wants to add a meal, they can use this tool.
    Args:
        meal_name (str): The name of the meal.
        grocery_items (str): Comma-separated list of grocery items.
        able_to_make_more_for_lunch (bool): Whether more can be made for lunch.
        cuisine (str): The type of cuisine.
    Returns:
        str: A confirmation message indicating that the meal has been added.

    Raises:
        ValueError: If meal_name, grocery_items, or cuisine is empty.
        ValueError: If the meal already exists in the database.
        TypeError: If able_to_make_more_for_lunch is not a boolean.
    """
    if not meal_name or not grocery_items or not cuisine:
        raise ValueError("Meal name, grocery items, and cuisine cannot be empty.")
    
    # Check
    meal_records = database.get_all_meal_records_from_db(DB_NAME)
    meal_names = [record[1] for record in meal_records]  # Assuming meal_name is the second element in the tuple
    if meal_name in meal_names:
        raise ValueError(f"Meal '{meal_name}' already exists in the database.")
    
    if not isinstance(able_to_make_more_for_lunch, bool):
        raise TypeError("able_to_make_more_for_lunch must be a boolean value.")
    
    # Add the meal to the database
    database.add_meal_to_db(meal_name, grocery_items, able_to_make_more_for_lunch, cuisine, DB_NAME)
    return f"Meal '{meal_name}' successfully added to the database."

@mcp.tool("write_meal_plan_to_json_file")
# Passing complex data structures like dicts or lists directly to MCP tools can sometimes lead to serialization issues.
# To avoid this, we can pass simpler data types (like strings or lists) and reconstruct the complex structure within the tool.
def write_meal_plan_to_json_file(lunch_list: list, dinner_list: list) -> str:
    """This tool writes the generated meal plan to a JSON file.
    The meal plan is provided as a dictionary
    This is useful for saving the meal plan for future reference or sharing.
    Args:
        lunch_list (list): A list of 7 meals for lunch, one for each day of the week.
        dinner_list (list): A list of 7 meals for dinner, one for each day of the week.
    Returns:
        str: A confirmation message indicating that the meal plan has been written to the file.
    Raises:
        ValueError: If lunch_list or dinner_list does not contain exactly 7 meals.

    """

    file_path = "./meal_plan.json"

    if (len(lunch_list) != 7) or (len(dinner_list) != 7):
        raise ValueError("Both lunch and dinner lists must contain exactly 7 meals.")

    # Not adding any more rules here to give the agent more flexibility to cater to user prompts.

    meal_plan = {"Lunch": lunch_list, "Dinner": dinner_list}

    with open(file_path, 'w') as json_file:
        json.dump(meal_plan, json_file, indent=4)
    
    return f"Meal plan successfully written to file. Please refresh the Meal Plan tab to see the updated plan."

@mcp.tool("execute_query_on_database")
def execute_query_on_database(sql_query: str, sql_query_args: list) -> list:
    """This tool executes a SQL query on the database.
    Before trying this, check if any of the other tools can help you.
    This is a low-level tool that allows you to run any SQL query on the database.
    It is not recommended for regular use, as it does not provide any safety checks or validation.
    Use it only if you know what you are doing.
    It is useful for debugging or for running complex queries that are not supported by the other tools.
    It is also useful for running custom queries that are not part of the meal planner functionality.
    If you want to add a new meal, use the `add_meal_to_db` tool instead.
    If you want to clean up the database, use the `cleanup_database` tool instead.
    If you want to fetch all meal records, use the `get_all_meal_records_from_db` tool instead.
    Use this as the last resort for executing custom SQL queries.
    Args:
        sql_query (str): The SQL query to execute.
        sql_query_args (list): The arguments for the SQL query.
    Returns:
        list: The result of the query as a list of tuples.
    Raises:
        ValueError: If sql_query is empty or not a string.
        TypeError: If sql_query_args is not a list.
        TypeError: If the result is not a list as expected.
    """
    if not sql_query or not isinstance(sql_query, str):
        raise ValueError("SQL query cannot be empty and must be a string.")
    if not isinstance(sql_query_args, list):
        raise TypeError("SQL query arguments must be a list.")

    result = database.execute_query_on_database(sql_query, sql_query_args, DB_NAME)
    if not result:
        return ["Query executed successfully, but no results to return."]
    if not isinstance(result, list):
        raise TypeError("Query result is not a list as expected.")

    return result

@mcp.tool("cleanup_database")
def cleanup_database() -> str:
    """This tool cleans up the database by removing all records from the meals table.
    This is not recommended for regular use, as it will delete all meal records.
    Use it only if you want to reset the database or start fresh.
    Args:
        None
    Returns:
        str: A confirmation message indicating that the database has been cleaned up.
    """
    database.cleanup_database(DB_NAME)
    return "Successfully cleaned up the database."


if __name__ == "__main__":
    # Start the MCP server
    mcp.run(transport="stdio")