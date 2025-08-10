import inspect
from typing import Callable, Any

from .tool_registry import register_tool
from langchain_core.tools import tool

@tool
def create_tool(code: str) -> str:
    """
    Creates a new tool from a string of Python code and registers it in the tool registry.
    The code should define a single function.

    Args:
        code (str): The Python code that defines the new tool.

    Returns:
        str: A message indicating the tool was created successfully.
    """
    try:
        # Execute the code in a new scope
        local_scope = {}
        exec(code, globals(), local_scope)

        # Find the new function in the local scope
        new_tool = None
        for name, value in local_scope.items():
            if inspect.isfunction(value):
                new_tool = value
                break

        if new_tool is None:
            return "Error: No function defined in the provided code."

        # Decorate the new function with @tool
        decorated_tool = tool(new_tool)

        # Register the new tool
        tool_name = new_tool.__name__
        register_tool(tool_name, decorated_tool)

        return f"Tool '{tool_name}' created and registered successfully."
    except Exception as e:
        return f"Error creating tool: {e}"
