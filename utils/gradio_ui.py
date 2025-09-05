import gradio as gr
import utils.agent as agent_utils
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

    # Insert the new column at the beginning (index -2)
    df.insert(loc=0, column="Day", value=first_col)
    return df

def get_gradio_interface(agent) -> gr.Blocks:
    chat_tab = gr.ChatInterface(
        fn=lambda message, _history: str(agent.run(message)),
        type="messages",
        examples=["Fetch all the meals from the database", "Add a new meal to the database", "Generate a meal plan for the week"],
        title="Agent with MCP Tools to manage your Meal Plans",
        description="This is a simple agent that uses MCP tools to help you manage your meal plans. You can ask it to fetch all meals, add new meals, and more.",
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
          fn=display_plan,  # The function to call
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
            fn=display_meals,  # The function to call
            inputs=None,         # No inputs are needed for this function
            outputs=meal_tab     # The component to update``
          )

    demo = gr.TabbedInterface([plan_block, chat_tab, meal_block], ["Meal Plan", "Planning Agent", "Meals in Database"])
    return demo