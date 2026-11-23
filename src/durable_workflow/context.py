"""Context engineering pipeline: shape what each agent sees before it runs."""

from collections.abc import Callable

Stage = Callable[[list[str]], list[str]]


def dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    return [i for i in items if not (i in seen or seen.add(i))]


def keep_recent(n: int) -> Stage:
    return lambda items: items[-n:]


def truncate(max_chars: int) -> Stage:
    return lambda items: [i[:max_chars] for i in items]


class ContextPipeline:
    """Runs an ordered list of stages over notes and renders a context string."""

    def __init__(self, *stages: Stage):
        self.stages = stages

    def build(self, task: str, notes: list[str]) -> str:
        for stage in self.stages:
            notes = stage(notes)
        body = "\n".join(f"- {n}" for n in notes) or "- (none)"
        return f"Task: {task}\nRelevant notes:\n{body}"


DEFAULT_PIPELINE = ContextPipeline(dedupe, keep_recent(10), truncate(500))
