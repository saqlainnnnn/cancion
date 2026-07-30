from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from cancion.api.dependencies import get_api_key_service
from cancion.api.schemas.api_key import (
    ApiKeyResponse,
    CreateApiKeyRequest,
    UpdateApiKeyRequest,
)
from cancion.db.mappers.api_key import to_api_key_response
from cancion.domain.api_key import ApiKey
from cancion.services.api_key import ApiKeyService

router = APIRouter()


@router.get("/", response_model=list[ApiKeyResponse])
def list_api_keys(
    service: ApiKeyService = Depends(get_api_key_service),
):
    return [to_api_key_response(api_key) for api_key in service.list()]


@router.get("/{api_key_id}", response_model=ApiKeyResponse)
def get_api_key(
    api_key_id: UUID,
    service: ApiKeyService = Depends(get_api_key_service),
):
    api_key = service.get(api_key_id)

    if api_key is None:
        raise HTTPException(
            status_code=404,
            detail="API key not found",
        )

    return to_api_key_response(api_key)


@router.post(
    "/",
    response_model=ApiKeyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_api_key(
    request: CreateApiKeyRequest,
    service: ApiKeyService = Depends(get_api_key_service),
):
    api_key = ApiKey(
        agent_id=request.agent_id,
        name=request.name,
        key_hash=request.key_hash,
    )

    return to_api_key_response(service.create(api_key))


@router.put(
    "/{api_key_id}",
    response_model=ApiKeyResponse,
)
def update_api_key(
    api_key_id: UUID,
    request: UpdateApiKeyRequest,
    service: ApiKeyService = Depends(get_api_key_service),
):
    api_key = service.get(api_key_id)

    if api_key is None:
        raise HTTPException(
            status_code=404,
            detail="API key not found",
        )

    updated = ApiKey(
        id=api_key.id,
        agent_id=api_key.agent_id,
        name=request.name,
        key_hash=request.key_hash,
        status=api_key.status,
        created_at=api_key.created_at,
        updated_at=api_key.updated_at,
    )

    return to_api_key_response(service.update(updated))


@router.delete(
    "/{api_key_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_api_key(
    api_key_id: UUID,
    service: ApiKeyService = Depends(get_api_key_service),
):
    deleted = service.delete(api_key_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="API key not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
