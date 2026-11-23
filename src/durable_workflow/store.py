"""PostgreSQL run registry: durable record of workflow runs and outcomes."""

import os

import psycopg

SCHEMA = """
CREATE TABLE IF NOT EXISTS workflow_runs (
    thread_id   TEXT PRIMARY KEY,
    task        TEXT NOT NULL,
    status      TEXT NOT NULL,
    result      TEXT,
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""


class RunStore:
    def __init__(self, dsn: str | None = None):
        self.dsn = dsn or os.getenv("POSTGRES_DSN")

    @property
    def enabled(self) -> bool:
        return bool(self.dsn)

    def _exec(self, sql: str, params: tuple = ()) -> None:
        if not self.enabled:
            return
        with psycopg.connect(self.dsn) as conn:
            conn.execute(SCHEMA)
            conn.execute(sql, params)

    def record(self, thread_id: str, task: str, status: str, result: str | None = None) -> None:
        self._exec(
            """
            INSERT INTO workflow_runs (thread_id, task, status, result)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (thread_id) DO UPDATE
              SET status = EXCLUDED.status, result = EXCLUDED.result, updated_at = now()
            """,
            (thread_id, task, status, result),
        )
