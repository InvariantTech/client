from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.challenge_response import ChallengeResponse
from ...models.validation_error_response import ValidationErrorResponse
from typing import Dict
from ...models.base_error_response import BaseErrorResponse
from ...models.ui_status_response import UIStatusResponse
from ...models.user_tabs_config import UserTabsConfig


def _get_kwargs(
    organization_name: str,
    *,
    json_body: UserTabsConfig,
) -> Dict[str, Any]:
    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/{organization_name}/api/v1/ui".format(
            organization_name=organization_name,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        BaseErrorResponse, ChallengeResponse, UIStatusResponse, ValidationErrorResponse
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UIStatusResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ValidationErrorResponse.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = ChallengeResponse.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = BaseErrorResponse.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        BaseErrorResponse, ChallengeResponse, UIStatusResponse, ValidationErrorResponse
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    organization_name: str,
    *,
    client: AuthenticatedClient,
    json_body: UserTabsConfig,
) -> Response[
    Union[
        BaseErrorResponse, ChallengeResponse, UIStatusResponse, ValidationErrorResponse
    ]
]:
    """Set UI state

    Args:
        organization_name (str):
        json_body (UserTabsConfig):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BaseErrorResponse, ChallengeResponse, UIStatusResponse, ValidationErrorResponse]]
    """

    kwargs = _get_kwargs(
        organization_name=organization_name,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_name: str,
    *,
    client: AuthenticatedClient,
    json_body: UserTabsConfig,
) -> Optional[
    Union[
        BaseErrorResponse, ChallengeResponse, UIStatusResponse, ValidationErrorResponse
    ]
]:
    """Set UI state

    Args:
        organization_name (str):
        json_body (UserTabsConfig):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BaseErrorResponse, ChallengeResponse, UIStatusResponse, ValidationErrorResponse]
    """

    return sync_detailed(
        organization_name=organization_name,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    organization_name: str,
    *,
    client: AuthenticatedClient,
    json_body: UserTabsConfig,
) -> Response[
    Union[
        BaseErrorResponse, ChallengeResponse, UIStatusResponse, ValidationErrorResponse
    ]
]:
    """Set UI state

    Args:
        organization_name (str):
        json_body (UserTabsConfig):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BaseErrorResponse, ChallengeResponse, UIStatusResponse, ValidationErrorResponse]]
    """

    kwargs = _get_kwargs(
        organization_name=organization_name,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_name: str,
    *,
    client: AuthenticatedClient,
    json_body: UserTabsConfig,
) -> Optional[
    Union[
        BaseErrorResponse, ChallengeResponse, UIStatusResponse, ValidationErrorResponse
    ]
]:
    """Set UI state

    Args:
        organization_name (str):
        json_body (UserTabsConfig):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BaseErrorResponse, ChallengeResponse, UIStatusResponse, ValidationErrorResponse]
    """

    return (
        await asyncio_detailed(
            organization_name=organization_name,
            client=client,
            json_body=json_body,
        )
    ).parsed
