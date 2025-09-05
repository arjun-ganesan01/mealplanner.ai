import os
from typing import Any

from smolagents import InferenceClientModel, CodeAgent, DuckDuckGoSearchTool, MCPClient, TransformersModel
from mcp import StdioServerParameters

SERVE_WITH_HF = os.getenv("MEALPLAN_SERVE_WITH_HF") # Set to True if you want to use HF Infra to Serve the model

MCP_SERVER_PARAMETERS = StdioServerParameters(
    command="uv",
    args=["run", "--with", "mcp", "mcp", "run", "./utils/mcp_server.py"],
    env={"UV_PYTHON": "3.12", **os.environ},
    transport="streamable-http",
)

def initialize_mcp_client(server_parameters: StdioServerParameters = MCP_SERVER_PARAMETERS) -> MCPClient:
    """Initialize the MCP client with the server parameters."""
    mcp_client = MCPClient(server_parameters=server_parameters)
    return mcp_client

def get_prompt_template() -> Any:
    """Update the system prompt of the agent to include information about available tools.
    This helps the agent to understand what tools are available and how to use them.
    """
    import yaml
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(CURRENT_DIR, "prompt_templates.yaml"), 'r') as stream:
        prompt_templates = yaml.safe_load(stream)
        return prompt_templates

def initialize_agent(mcp_client: MCPClient) -> Any:
    """Initialize the agent with the MCP client and the model.
        Args:
        mcp_client (MCPClient): The MCP client to use for tool calls.
        Returns:
        Any: The initialized agent.
    """
    tools = mcp_client.get_tools()
    tools.append(DuckDuckGoSearchTool())
    print (f"Available tools: {[tool.name for tool in tools]}")

    model_id = "Qwen/Qwen3-30B-A3B-Instruct-2507"

    if ( (SERVE_WITH_HF is not None) and SERVE_WITH_HF.lower() == "true"):
        model = InferenceClientModel(model_id=model_id, token=os.getenv("HUGGINGFACE_API_TOKEN"))
    else:
        model = TransformersModel(
            model_id=model_id,
            device_map="cpu",
            max_new_tokens=10000,
        )

    prompt_templates = get_prompt_template()

    agent = CodeAgent(tools=tools,
                        model=model,
                        additional_authorized_imports=["json", "ast", "urllib", "base64", "random"],
                        stream_outputs=True,
                        max_print_outputs_length= 5000,
                        max_steps=10,
                        prompt_templates=prompt_templates,
                    )
    return agent