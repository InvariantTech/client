from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from typing import List
from ...models.user import User
from typing import Dict
from ...models.challenge_response import ChallengeResponse
from ...models.validation_error_response import ValidationErrorResponse


def _get_kwargs() -> Dict[str, Any]:
    return {
        "method": "post",
        "url": "/api/v1/login/get_instances",
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ChallengeResponse, List["User"], ValidationErrorResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = User.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ValidationErrorResponse.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ChallengeResponse.from_dict(response.json())

        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ChallengeResponse, List["User"], ValidationErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[ChallengeResponse, List["User"], ValidationErrorResponse]]:
    """List instances available to the current login

     List instances where this login is associated with an active user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChallengeResponse, List['User'], ValidationErrorResponse]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ChallengeResponse, List["User"], ValidationErrorResponse]]:
    """List instances available to the current login

     List instances where this login is associated with an active user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChallengeResponse, List['User'], ValidationErrorResponse]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[ChallengeResponse, List["User"], ValidationErrorResponse]]:
    """List instances available to the current login

     List instances where this login is associated with an active user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChallengeResponse, List['User'], ValidationErrorResponse]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ChallengeResponse, List["User"], ValidationErrorResponse]]:
    """List instances available to the current login

     List instances where this login is associated with an active user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChallengeResponse, List['User'], ValidationErrorResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
