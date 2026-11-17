from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from agent_state import ITSupportState
from agent import agent_node
from tool_node import tool_execution_node
from ticket_approval import ticket_approval_node
from langchain_core.messages import ToolMessage, AIMessage
def should_continue(state: ITSupportState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END
def route_after_tools(state: ITSupportState):
    if state.get("awaiting_confirmation", False):
        return "approval"
    messages = state["messages"]
    last_ai_message = next(
        (
            message
            for message in reversed(messages)
            if isinstance(message, AIMessage)
            and message.tool_calls
        ),
        None
    )
    if not last_ai_message:
        return "agent"
    tool_names = [
        call["name"]
        for call in last_ai_message.tool_calls
    ]
    if (
        tool_names == ["knowledge_base_search"]
        and isinstance(messages[-1], ToolMessage)
    ):
        return "grounded_answer"
    if (
        "knowledge_base_search" in tool_names
        and "ticket_status_lookup" in tool_names
    ):
        return "multi_tool_answer"
    return "agent"
def grounded_answer_node(state: ITSupportState):
    """
    Return the grounded knowledge answer directly
    without asking the LLM to rewrite it.
    """
    last_message = state["messages"][-1]
    return {
        "messages": [
            AIMessage(content=last_message.content)
        ]
    }
def multi_tool_answer_node(state: ITSupportState):
    """
    Combine knowledge-base and ticket-status results
    without allowing the LLM to rewrite them.
    """
    messages = state["messages"]
    last_ai_message = next(
        (
            message
            for message in reversed(messages)
            if isinstance(message, AIMessage)
            and message.tool_calls
        ),
        None
    )
    if not last_ai_message:
        return {
            "messages": [
                AIMessage(content="Unable to retrieve tool results.")
            ]
        }
    tool_names = {
        call["id"]: call["name"]
        for call in last_ai_message.tool_calls
    }
    results = {}
    for message in messages:
        if (
            isinstance(message, ToolMessage)
            and message.tool_call_id in tool_names
        ):
            results[tool_names[message.tool_call_id]] = message.content
    sections = []
    if "knowledge_base_search" in results:
        sections.append(
            "IT KNOWLEDGE BASE RESULT:\n\n"
            + results["knowledge_base_search"]
        )
    if "ticket_status_lookup" in results:
        sections.append(
            "TICKET STATUS RESULT:\n\n"
            + results["ticket_status_lookup"]
        )
    final_answer = ("\n\n" + ("-" * 50) + "\n\n").join(sections)
    return {
        "messages": [
            AIMessage(content=final_answer)
        ]
    }
workflow = StateGraph(ITSupportState)
workflow.add_node("grounded_answer", grounded_answer_node)
workflow.add_node(
    "multi_tool_answer",
    multi_tool_answer_node
)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_execution_node)
workflow.add_node("approval", ticket_approval_node)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)
workflow.add_conditional_edges(
    "tools",
    route_after_tools,
    {
        "approval": "approval",
        "grounded_answer": "grounded_answer",
        "multi_tool_answer": "multi_tool_answer",
        "agent": "agent"
    }
)
workflow.add_edge("multi_tool_answer", END)
workflow.add_edge("grounded_answer", END)
workflow.add_edge("approval", END)
checkpointer = InMemorySaver()
agent_graph = workflow.compile(
    checkpointer=checkpointer
)
print("Complete IT Support Agent Graph compiled successfully!")