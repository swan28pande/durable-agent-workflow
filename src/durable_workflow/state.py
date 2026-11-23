import operator
from typing import Annotated, TypedDict


class WorkflowState(TypedDict, total=False):
    """Shared state passed between agent nodes and checkpointed after each step."""

    task: str
    plan: list[str]
    notes: Annotated[list[str], operator.add]
    context: str
    result: str
