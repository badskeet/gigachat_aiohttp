from http import HTTPStatus
from typing import Any, Dict, Optional

import aiohttp

from gigachat.api.utils import build_headers
from gigachat.exceptions import AuthenticationError, ResponseError


def _get_kwargs(
    *,
    thread_id: str,
    access_token: Optional[str] = None,
) -> Dict[str, Any]:
    headers = build_headers(access_token)
    params = {
        "method": "POST",
        "url": "/threads/delete",
        "json": {
            "thread_id": thread_id,
        },
        "headers": headers,
    }
    return params


async def _build_response(response: aiohttp.ClientResponse) -> bool:
    if response.status == HTTPStatus.OK:
        return True
    elif response.status == HTTPStatus.UNAUTHORIZED:
        content = await response.read()
        raise AuthenticationError(str(response.url), response.status, content, response.headers)
    else:
        content = await response.read()
        raise ResponseError(str(response.url), response.status, content, response.headers)


def sync(
    client: aiohttp.ClientSession,
    *,
    thread_id: str,
    access_token: Optional[str] = None,
) -> bool:
    """Удаляет тред"""
    kwargs = _get_kwargs(thread_id=thread_id, access_token=access_token)
    response = client.request(**kwargs)
    return _build_response(response)


async def asyncio(
    client: aiohttp.ClientSession,
    *,
    thread_id: str,
    access_token: Optional[str] = None,
) -> bool:
    """Удаляет тред"""
    kwargs = _get_kwargs(thread_id=thread_id, access_token=access_token)
    async with client.request(**kwargs) as response:
        return await _build_response(response)
