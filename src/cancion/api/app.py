from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cancion.api.routes import agents, api_keys
from cancion.api.routes.contracts import router as contracts_router
from cancion.api.routes.decisions import router as decisions_router
from cancion.api.routes.governance import router as governance_router
from cancion.api.routes.organizations import router as organization_router

app = FastAPI(
    title="Cancion",
    description="AI Agent Spending Governance API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    contracts_router,
    prefix="/contracts",
    tags=["Contracts"],
)

app.include_router(
    decisions_router,
    prefix="/decisions",
    tags=["Decisions"],
)

app.include_router(
    governance_router,
    prefix="/governance",
    tags=["Governance"],
)

app.include_router(
    organization_router,
    prefix="/organizations",
    tags=["Organizations"],
)

app.include_router(
    agents.router,
    prefix="/agents",
    tags=["Agents"],
)

app.include_router(
    api_keys.router,
    prefix="/api-keys",
    tags=["API Keys"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Cancion API is running!"}
