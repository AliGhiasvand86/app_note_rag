# Agent graph

from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from src.llm import get_llm
from src.agent.state import AgentState
from src.agent.tools import tools


llm = get_llm().bind_tools(tools)


SYSTEM_PROMPT = """
You are an AI assistant for a note-taking application.

You can perform these operations on the authenticated user's notes:

- Create a note using its title and content.
- Summarize a note using its title.
- Delete a note using its title.
- Search the user's notes and answer questions using the retrieved information.

Use the appropriate tool whenever the user requests one of these operations.

For summarize and delete operations, the user identifies the note by its title.
Never ask the user for a note ID.

For questions about information contained in the user's notes, use the search notes tool before answering.

The authenticated user's ID is provided by the application runtime.
Never ask the user for their user ID.

When answering questions based on the user's notes, use only the information returned by the search notes tool.
Do not invent information or claim that information exists in the user's notes when it was not retrieved.

If the search notes tool does not return relevant information, clearly state that the information could not be found in the user's notes.
"""


def call_model(state: AgentState):
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"],
    ]

    response = llm.invoke(messages)

    return {"messages": [response]}


tool_node = ToolNode(tools)

graph_builder = StateGraph(AgentState)

graph_builder.add_node("agent", call_model)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "agent")

graph_builder.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",
        END: END,
    },
)

graph_builder.add_edge("tools", "agent")

graph = graph_builder.compile()