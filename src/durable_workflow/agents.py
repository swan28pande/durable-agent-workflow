"""Agent nodes. Each is a plain function State -> partial State.

These are deterministic stubs; swap in LLM calls without changing the graph.
"""

from .context import DEFAULT_PIPELINE
from .state import WorkflowState


def planner(state: WorkflowState) -> WorkflowState:
    task = state["task"]
    plan = [f"research: {task}", f"draft answer for: {task}"]
    return {"plan": plan, "notes": [f"planner created {len(plan)} steps"]}


def context_builder(state: WorkflowState) -> WorkflowState:
    return {"context": DEFAULT_PIPELINE.build(state["task"], state.get("notes", []))}


def researcher(state: WorkflowState) -> WorkflowState:
    findings = [f"finding for '{step}'" for step in state.get("plan", [])]
    return {"notes": findings}


def writer(state: WorkflowState) -> WorkflowState:
    summary = f"Result for '{state['task']}' based on:\n{state.get('context', '')}"
    return {"result": summary, "notes": ["writer produced result"]}
