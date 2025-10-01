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

### 3. Select Model backend

The default model is set to `Qwen/Qwen3-30B-A3B-Instruct-2507` and can be customized with `MODEL_ID` environment variable.

To use HuggingFace Inference Infrastructure, set these environment variables before running the app:

```sh
export MEALPLAN_MODEL_TYPE=InferenceClientModel HUGGINGFACE_API_TOKEN=YOUR_HF_TOKEN
```

To use a local OpenAI compatible API server, set these environment variables:
```sh
export MEALPLAN_MODEL_TYPE=OpenAIServerModel OPENAI_BASE_URL=YOUR_BASE_URL OPENAI_API_KEY=YOUR_API_KEY
```

---

Note that if neither options are not used, the app downloads the model from the HuggingFace Hub
to your local machine and runs inference using your local hardware.

### 4. Run the App

```sh
python app.py
```

<details>

<summary>Running the app in a development container</summary>

- A [Dev Container](https://containers.dev/) definition for the app is [available](.devcontainer/devcontainer.json) for use.
- Follow
  https://code.visualstudio.com/docs/devcontainers/containers#_installation or
  https://devpod.sh/docs/getting-started/install to install a dev container
  implementation
- Make sure docker or podman is configured on the host.
- For devpod, run `devpod up .` to start and `devpod ssh .` to enter the container.
- By default, uv and pip dependencies will be automatically installed.
- To start application, run `uv run ./app.py` inside the container.

</details>

Open http://127.0.0.1:7860/ on your favorite browser to launch the Gradio interface.

The Gradio interface will have three tabs:
- **Meal Plan**: View and refresh your weekly meal plan.
- **Planning Agent**: Chat with the CodeAgent to manage meal plans using MCP tools.
- **Meals in Database**: View and refresh the list of meals in your database.

---

## Future Work

- Right now, the search_tool doesn't fully work as expected since the LLM doesn't know how to parse the results.
- Need to add some logic and some examples for this

## Notes

- The agent and MCP tools are defined in `utils/agent.py` and `utils/mcp_server.py`.
- The weekly plan is stored in `meal_plan.json`, and the meal database in `meals_database.db`.
- For prompt templates and agent logic, see `utils/prompt_templates.yaml`.
- The agent also includes a DuckDuckGo search tool, allowing it to fetch information from the web to assist with meal planning and related queries.

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.
