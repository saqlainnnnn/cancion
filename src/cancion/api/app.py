from fastapi import FastAPI

from cancion.api.routes.contracts import router as contracts_router
from cancion.api.routes.governance import router as governance_router

app = FastAPI(
    title="Cancion",
    description="AI Agent Spending Governance API",
    version="0.1.0",
)

app.include_router(
    contracts_router,
    prefix="/contracts",
    tags=["Contracts"],
)

app.include_router(
    governance_router,
    prefix="/governance",
    tags=["Governance"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Cancion API is running!"}
