# Meal Planner App

## Summary

This app provides an interactive Gradio interface for planning weekly meals and managing a meal database. It features a conversational CodeAgent powered by MCP tools, allowing you to automate meal planning, add new meals, fetch meals from the database, and run custom queries — all through natural language.

**Key Features:**
- View and refresh your weekly meal plan.
- Browse and update the database of meals.
- Use the Planning Agent (CodeAgent) to automate meal planning and management with MCP and Search tools.

---

## Setup Instructions

### 1. Create and Activate a Virtual Environment

```sh
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Requirements Using uv

If you don't have [uv](https://github.com/astral-sh/uv), install it first.
[Installation steps here](https://docs.astral.sh/uv/getting-started/installation/)

Then install dependencies:

```sh
uv pip install -r requirements.txt
```

---

### 3. (Optional) Use HuggingFace Inference Infrastructure

To serve the agent using HuggingFace, set the environment variable before running the app:

```sh
export MEALPLANNER_SERVE_WITH_HF=true
export HF_TOKEN=<your HF Token>
```

---

### 4. Run the App

```sh
python app.py
```

Open http://127.0.0.1:7860/ on your favorite browser to launch the Gradio interface.

The Gradio interface will have three tabs:
- **Meal Plan**: View and refresh your weekly meal plan.
- **Planning Agent**: Chat with the CodeAgent to manage meal plans using MCP tools.
- **Meals in Database**: View and refresh the list of meals in your database.

---

## Notes

- The agent and MCP tools are defined in `utils/agent.py` and `utils/mcp_server.py`.
- The weekly plan is stored in `meal_plan.json`, and the meal database in `meals_database.db`.
- For prompt templates and agent logic, see `utils/prompt_templates.yaml`.
- The agent also includes a DuckDuckGo search tool, allowing it to fetch information from the web to assist with meal planning and related queries.

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.