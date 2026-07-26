from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_contracts() -> list:
    return []


@router.get("/{contract_id}")
def get_contract(contract_id: str) -> dict[str, str]:
    return {"contract_id": contract_id}


@router.post("/")
def create_contract() -> dict[str, str]:
    return {"message": "Create contract endpoint"}


@router.delete("/{contract_id}")
def delete_contract(contract_id: str) -> dict[str, str]:
    return {"deleted": contract_id}
