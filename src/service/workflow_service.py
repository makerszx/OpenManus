"""Workflow service for managing agent workflow execution."""

import asyncio
from typing import AsyncGenerator, Dict, List

from src.workflow.graph import build_graph
from src.prompts.template import OpenManusPromptTemplate
from src.memory import save_state, load_state


async def run_agent_workflow(
    messages: List[Dict[str, str]], debug: bool = False
) -> AsyncGenerator[Dict[str, str], None]:
    """Run the agent workflow with the given messages.

    Args:
        messages: List of chat messages
        debug: Whether to enable debug logging

    Yields:
        Event data for SSE streaming
    """
    # Load state from memory
    state = load_state()
    state["messages"].extend(messages)

    # Initialize workflow graph
    workflow = build_graph()

    # Format messages with system prompt
    state["messages"] = OpenManusPromptTemplate.apply_prompt_template(
        "coordinator", state
    )

    # Run workflow
    async for event in workflow.astream(state):
        # Save state to memory
        save_state(event)

        yield {
            "event": "message",
            "data": {"content": event.get("content", ""), "role": "assistant"}
        }
        # Small delay to avoid overwhelming the client
        await asyncio.sleep(0.1)