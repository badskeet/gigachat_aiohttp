from typing import Any, Dict, Union

import aiohttp
import requests

from gigachat.api.utils import build_headers, build_response, build_response_async
from gigachat.models import Token


def _get_kwargs(
    *,
    user: str,
    password: str,
) -> Dict[str, Any]:
    headers = build_headers()

    return {
        "method": "POST",
        "url": "/token",
        "auth": (user, password),
        "headers": headers,
    }


def sync(
    client: Union[aiohttp.ClientSession, requests.Session],
    *,
    user: str,
    password: str,
) -> Token:
    kwargs = _get_kwargs(user=user, password=password)
    response = client.request(**kwargs)
    return build_response(response, Token)


async def asyncio(
    client: aiohttp.ClientSession,
    *,
    user: str,
    password: str,
) -> Token:
    kwargs = _get_kwargs(user=user, password=password)
    async with client.request(**kwargs) as response:
        return await build_response_async(response, Token)
