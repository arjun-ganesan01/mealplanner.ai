import gradio as gr
import pandas as pd

def display_meals() -> pd.DataFrame:
    from utils.database import get_all_meal_records_from_db
    meal_records = get_all_meal_records_from_db()
    df = pd.DataFrame(meal_records, columns=["ID", "Meal Name", "Grocery Items", "Able to Make More for Lunch", "Cuisine"])
    return df

def display_plan() -> pd.DataFrame:
    # Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
    # Load the data with lines=True for line-delimited JSON
    df = pd.read_json('meal_plan.json')
    first_col = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Insert the new column at the beginning 
    df.insert(loc=0, column="Day", value=first_col)
    return df

def display_grocery_list()-> pd.DataFrame:
    """Reads the meal_plan.json, gets the meals in the current week's plan.
    Then gets the grocery items for the meals.
    Counts the grocery items across all meals
    and creates a grocery list with quantities.
    Finally, sorts the grocery list alphabetically by item name.
    Returns the grocery list as a dataframe.
    Args:
        None
    Returns:
        pd.DataFrame: A dataframe with two columns: "Grocery Item" and "Quantity
    """
    meal_plan_df = pd.read_json('meal_plan.json')
    meal_names = meal_plan_df.values.flatten().tolist()
    sql_query = f"SELECT grocery_items FROM meals WHERE meal_name IN ({', '.join(['?']*len(meal_names))})"
    from utils.database import execute_query_on_database
    grocery_dict = {}
    grocery_items = execute_query_on_database(sql_query, tuple(meal_names))
    for items_in_one_meal in grocery_items:
        # Each element is a tuple with one string separated by commas
        for item in items_in_one_meal[0].split(', '):
            if item in grocery_dict:
                grocery_dict[item] += 1
            else:
                grocery_dict[item] = 1
    grocery_items_df = pd.DataFrame(grocery_dict.items(), columns=["Grocery Item", "Quantity"])
    grocery_items_df = grocery_items_df.sort_values(by="Grocery Item").reset_index(drop=True)
    return grocery_items_df

def get_gradio_interface(agent) -> gr.Blocks:
    chat_tab = gr.ChatInterface(
        fn=lambda message, _history: str(agent.run(message)),
        type="messages",
        examples=["Fetch all the meals from the database", "Add a new meal to the database", "Generate a meal plan for the week"],
        title="Agent with MCP Tools to manage your Meal Plans",
        description="This is a simple agent that uses MCP tools to help you manage your meal plans. You can ask it to fetch all meals, add new meals, and more.",
    )

    with gr.Blocks() as grocery_block:
        plan_tab = gr.DataFrame(headers=["Groccery Item", "Quantity"],
                                  value=display_grocery_list(),
                                  interactive=True,
                                  label="Grocery List")

        # Define a button to trigger the rerun
        refresh_button = gr.Button("Refresh Table")
        
        # Bind the button's click event to the update function
        refresh_button.click(
          fn=display_grocery_list,     # The function to call
          inputs=None,                 # No inputs are needed for this function
          outputs=plan_tab             # The component to update``
        )

    with gr.Blocks() as plan_block:
        plan_tab = gr.DataFrame(headers=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                  value=display_plan(),
                                  interactive=True,
                                  label="Weekly Meal Plan")

        # Define a button to trigger the rerun
        refresh_button = gr.Button("Refresh Table")
        
        # Bind the button's click event to the update function
        refresh_button.click(
          fn=display_plan,     # The function to call
          inputs=None,         # No inputs are needed for this function
          outputs=plan_tab     # The component to update``
        )

    with gr.Blocks() as meal_block:
        meal_tab = gr.DataFrame(headers=["ID", "Meal Name", "Grocery Items", "Able to Make More for Lunch", "Cuisine"],
                                  value=display_meals(),
                                  interactive=True,
                                  label="Meals in Database")

        # Define a button to trigger the rerun
        refresh_button = gr.Button("Refresh Table")
        
        # Bind the button's click event to the update function
        refresh_button.click(
            fn=display_meals,    # The function to call
            inputs=None,         # No inputs are needed for this function
            outputs=meal_tab     # The component to update``
          )

    demo = gr.TabbedInterface([plan_block, grocery_block, chat_tab, meal_block], ["Meal Plan", "Grocery List", "Planning Agent", "Meals in Database"])
    return demo