from typing import Dict
from langchain_core.runnables import Runnable

# A dictionary to store all the tools
_tools: Dict[str, Runnable] = {}

def register_tool(name: str, tool: Runnable):
    """
    Registers a new tool in the tool registry.

    Args:
        name (str): The name of the tool.
        tool (Runnable): The tool runnable.
    """
    _tools[name] = tool

def get_tool(name: str) -> Runnable:
    """
    Gets a tool from the tool registry.

    Args:
        name (str): The name of the tool.

    Returns:
        Runnable: The tool runnable.
    """
    return _tools.get(name)

def get_all_tools() -> Dict[str, Runnable]:
    """
    Gets all the tools from the tool registry.

    Returns:
        Dict[str, Runnable]: A dictionary of all the tools.
    """
    return _tools
