
from langchain_tools import it_support_tools
from langchain_core.messages import ToolMessage


# Map tool names to their corresponding Python functions.
tools_by_name = {
    tool.name: tool
    for tool in it_support_tools
}


def tool_execution_node(state):

    last_message = state["messages"][-1]

    tool_results = []

    pending_ticket_description = None
    awaiting_confirmation = False

    # Stores the original knowledge-base search result.
    last_grounded_result = None

    for tool_call in last_message.tool_calls:

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        selected_tool = tools_by_name.get(tool_name)

        if selected_tool is None:
            result = f"Unknown tool: {tool_name}"

        else:
            try:
                # Execute the selected tool.
                result = selected_tool.invoke(tool_args)

                # Preserve the original RAG result.
                if tool_name == "knowledge_base_search":
                    last_grounded_result = result

                # Handle support ticket requests.
                if tool_name == "request_support_ticket":

                    issue = tool_args.get(
                        "issue_description", ""
                    ).strip()

                    if not issue:
                        result = (
                            "Ticket request failed: "
                            "issue description is empty."
                        )

                    elif pending_ticket_description is not None:
                        result = (
                            "Only one ticket request can be "
                            "processed at a time."
                        )

                    else:
                        pending_ticket_description = issue
                        awaiting_confirmation = True

                        result = (
                            "Ticket request prepared successfully. "
                            "Waiting for user approval before creation."
                        )

            except Exception as error:

                result = f"Tool execution failed: {error}"

        # Send tool result back to LangGraph.
        tool_message = ToolMessage(
            content=str(result),
            tool_call_id=tool_call["id"]
        )

        tool_results.append(tool_message)

    # Prepare state updates.
    updates = {
        "messages": tool_results
    }

    # Save pending ticket information.
    if pending_ticket_description is not None:

        updates["pending_ticket_description"] = (
            pending_ticket_description
        )

        updates["awaiting_confirmation"] = True

    # Save the original knowledge-base result.
    if last_grounded_result is not None:

        updates["last_grounded_result"] = last_grounded_result

    return updates
