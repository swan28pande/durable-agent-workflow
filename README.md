# Durable Agent Workflow Engine

A minimal, durable graph-based workflow engine for multi-agent orchestration, built on LangGraph.

- **LangGraph** graph of agent nodes (`planner → researcher → context_builder → writer`)
- **Redis** checkpointing after every node, so runs resume by `thread_id` after a crash
- **PostgreSQL** run registry (`workflow_runs` table) for status and results
- **Context engineering pipeline** — composable stages (dedupe, recency window, truncation) that shape what each agent sees

## Quickstart

Requires Python 3.11–3.14 (tested on 3.12).

```bash
docker compose up -d
python -m venv .venv && source .venv/bin/activate
pip install -e .
cp .env.example .env && export $(cat .env | xargs)

durable-workflow "Summarize the tradeoffs of event sourcing"
durable-workflow --thread <thread-id>   # resume from last checkpoint
```

Without `REDIS_URL` it falls back to an in-memory checkpointer; without `POSTGRES_DSN` run recording is skipped.

## Layout

```
src/durable_workflow/
  graph.py       # StateGraph wiring
  agents.py      # agent nodes (stubs — swap in LLM calls)
  context.py     # context engineering pipeline
  checkpoint.py  # Redis checkpointer
  store.py       # Postgres run registry
  cli.py         # entry point
```
