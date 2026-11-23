"""Redis-backed checkpointing so workflows resume after crashes or restarts."""

import os
from contextlib import contextmanager

from langgraph.checkpoint.memory import MemorySaver


@contextmanager
def get_checkpointer(redis_url: str | None = None):
    url = redis_url or os.getenv("REDIS_URL")
    if not url:
        yield MemorySaver()
        return
    from langgraph.checkpoint.redis import RedisSaver

    with RedisSaver.from_conn_string(url) as saver:
        saver.setup()
        yield saver
