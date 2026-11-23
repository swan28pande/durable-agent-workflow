import argparse
import uuid

from .checkpoint import get_checkpointer
from .graph import build_workflow
from .store import RunStore


def main() -> None:
    p = argparse.ArgumentParser(description="Run or resume a durable workflow")
    p.add_argument("task", nargs="?", help="Task to run (omit with --thread to resume)")
    p.add_argument("--thread", help="Thread id to resume or reuse")
    args = p.parse_args()

    thread_id = args.thread or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    store = RunStore()

    with get_checkpointer() as saver:
        app = build_workflow(saver)
        if args.task:
            store.record(thread_id, args.task, "running")
            final = app.invoke({"task": args.task}, config)
        else:
            # Resume from last checkpoint: invoking with None continues pending nodes.
            final = app.invoke(None, config)

        store.record(thread_id, final.get("task", ""), "completed", final.get("result"))
        print(f"thread: {thread_id}\n\n{final.get('result')}")


if __name__ == "__main__":
    main()
