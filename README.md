# Cancion

**A governance layer for AI agent payments.**

Cancion sits between AI agents and the vendors/services they spend money on. An agent expresses a spending intent in natural language (e.g. *"renew my Netflix subscription for $15/month"*), Cancion parses that intent into a structured **Contract**, and every subsequent spend request from the agent is evaluated against that contract's rules before it's allowed to go through.

The goal is a deterministic, auditable policy engine that sits in front of agentic payments — not a payment processor itself.

> ⚠️ **Status: early / active development.** The domain, governance, and persistence layers are functional and tested. The API layer, audit trail, and authentication are still being built out. See [Roadmap](#roadmap) below.

---

## How it works

```
"renew Netflix for $15 monthly"
          │
          ▼
   Intent Parser (regex-based, deterministic)
          │
          ▼
      Intent  →  IntentBuilder validates required fields
          │
          ▼
   ContractFactory  →  Contract (vendor, action, max_amount, frequency, approval_mode)
          │
          ▼
   ContractRepository  →  persisted (SQLAlchemy / Postgres)


Later, an agent requests to spend:

   SpendRequest (vendor, action, amount)
          │
          ▼
   GovernanceEngine runs a pipeline of Rules against the Contract:
     • VendorRule    — does the vendor match?
     • ActionRule    — does the action match?
     • AmountRule    — is the amount within the contract limit?
     • StatusRule    — is the contract still active?
     • ApprovalRule  — does this contract require manual approval?
          │
          ▼
      Decision: APPROVE / DENY / ESCALATE  (with reasons)
```

## Architecture

Cancion follows a clean, layered architecture — each layer only depends on the one below it, and the governance/domain core has no framework dependencies at all.

```
src/cancion/
├── domain/          # Pure data models: Intent, Contract, Decision — no framework code
├── governance/       # Rule engine: GovernanceEngine, Rule protocol, individual policies
│   └── policies/      # VendorRule, ActionRule, AmountRule, StatusRule, ApprovalRule
├── intent/           # Natural-language → Intent parsing
│   └── regex/          # Deterministic keyword/regex-based parser (MVP; pluggable via IntentParser protocol)
├── services/         # Application services orchestrating domain + repositories
├── repositories/     # Persistence interfaces
├── db/               # SQLAlchemy models, session management, mappers (domain ↔ ORM)
├── api/               # FastAPI app, routes, request/response schemas
├── core/              # Configuration (pydantic-settings) and structured logging
└── common/           # Shared value objects and enums (Money, Action, Frequency, ApprovalMode)
```

Because `domain` and `governance` don't depend on FastAPI or SQLAlchemy, the policy engine can be tested and reasoned about in complete isolation from the web/persistence layers.

## Tech stack

- **Python 3.13**
- **FastAPI** — API layer
- **SQLAlchemy 2.x** + **Alembic** — persistence and migrations
- **Pydantic v2** / **pydantic-settings** — validation and configuration
- **structlog** — structured logging
- **pytest** / **pytest-cov** / **coverage** — testing
- **ruff** / **mypy** / **pre-commit** — linting, typing, and CI hygiene
- **uv** — dependency and environment management

## Getting started

```bash
# Install dependencies
uv sync

# Copy environment config
cp .env.example .env

# Run database migrations
uv run alembic upgrade head

# Start the API
uv run uvicorn cancion.api.app:app --reload --port 8015
```

The API will be available at `http://localhost:8015`, with interactive docs at `http://localhost:8015/docs`.

### Frontend UI

A lightweight React frontend was added under `frontend/` for local development:

```bash
cd frontend
npm install
npm run dev
```

The frontend will run on `http://localhost:5174` (or the first available host), and the backend should be running on `http://localhost:8015`.

## Feature flow documentation

See [docs/feature-flows.md](docs/feature-flows.md) for user flows and internal implementation maps for:

- Contract creation
- Active contract listing
- Contract deactivation / soft delete
- Inactive contract history
- Spend evaluation
- Governance policy evaluation pipeline

```bash
cd frontend
npm install
npm run dev
```

Then open `http://localhost:5173`.
The API will be available at `http://localhost:8015`.
### Running tests

```bash
uv run pytest
```

## Roadmap

Cancion is being built in phases. Phases 1–6 (foundation, intent parsing, domain, governance engine, persistence, application services) are complete and tested. Current focus:

- **Phase 7 — FastAPI**: wiring the API layer to the existing service layer, contract lifecycle endpoints, cumulative spend enforcement (`FrequencyRule` + spend ledger), idempotency, and error handling.
- **Phase 8 — Audit & Governance History**: permanent, queryable decision records for every governance evaluation.
- **Phase 9 — Identity & Authorization**: agent authentication, contract ownership, per-agent rate limiting.
- **Phase 10 — External Integrations**: payment execution and policy synchronization.
- **Phase 11 — Production Readiness**: observability, CI/CD, deployment.

Cross-cutting concerns tracked throughout: optimistic concurrency (via `Contract.version`), currency validation, and idempotency on write endpoints.

## Design principles

- **Deterministic over clever.** The governance engine is a pure rule pipeline with no hidden state — every decision is explainable by the list of rules that fired.
- **Domain isolation.** Business logic (`domain`, `governance`) has zero framework dependencies, so it can be tested, reasoned about, and evolved independently of the API or database.
- **Auditability first.** Every governance decision is designed to be traceable back to the contract and rules that produced it (in progress — see Phase 8).

## License

TBD.
