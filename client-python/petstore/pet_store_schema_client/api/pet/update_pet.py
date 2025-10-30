from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.pet_status import PetStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    pet_id: int,
    *,
    name: str | Unset = UNSET,
    status: PetStatus | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["name"] = name

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/pet/{pet_id}",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | None:
    if response.status_code == 200:
        return None

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    pet_id: int,
    *,
    client: AuthenticatedClient | Client,
    name: str | Unset = UNSET,
    status: PetStatus | Unset = UNSET,
) -> Response[Any]:
    """Updates a pet in the store

    Args:
        pet_id (int):
        name (str | Unset):
        status (PetStatus | Unset): pet status in the store

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        pet_id=pet_id,
        name=name,
        status=status,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    pet_id: int,
    *,
    client: AuthenticatedClient | Client,
    name: str | Unset = UNSET,
    status: PetStatus | Unset = UNSET,
) -> Response[Any]:
    """Updates a pet in the store

    Args:
        pet_id (int):
        name (str | Unset):
        status (PetStatus | Unset): pet status in the store

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        pet_id=pet_id,
        name=name,
        status=status,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
