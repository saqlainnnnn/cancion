from fastapi import APIRouter

router = APIRouter()


@router.post("/evaluate")
def evaluate() -> dict[str, str]:
    return {"message": "Governance evaluation endpoint"}
