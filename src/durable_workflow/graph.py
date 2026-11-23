from langgraph.graph import END, START, StateGraph

from . import agents
from .state import WorkflowState


def build_workflow(checkpointer=None):
    """planner -> researcher -> context_builder -> writer, checkpointed per node."""
    g = StateGraph(WorkflowState)
    g.add_node("planner", agents.planner)
    g.add_node("researcher", agents.researcher)
    g.add_node("context_builder", agents.context_builder)
    g.add_node("writer", agents.writer)

    g.add_edge(START, "planner")
    g.add_edge("planner", "researcher")
    g.add_edge("researcher", "context_builder")
    g.add_edge("context_builder", "writer")
    g.add_edge("writer", END)
    return g.compile(checkpointer=checkpointer)
