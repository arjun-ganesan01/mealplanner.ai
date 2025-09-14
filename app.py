#!/usr/bin/env python3

import os

import utils.gradio_ui as gradio_ui
import utils.agent as agent_utils

def main():
    SERVER_NAME = os.getenv('SERVER_NAME')

    try:
      mcp_client = agent_utils.initialize_mcp_client()
      agent = agent_utils.initialize_agent(mcp_client)
      demo = gradio_ui.get_gradio_interface(agent)

      demo.launch(server_name=SERVER_NAME)
    finally:
      mcp_client.disconnect()

if __name__ == "__main__":
    main()
