import json
from http import HTTPStatus
from typing import Any, Dict, List, Optional

import aiohttp

from gigachat.api.utils import build_headers
from gigachat.exceptions import AuthenticationError, ResponseError
from gigachat.models import TokensCount


def _get_kwargs(
    *,
    input_: List[str],
    model: str,
    access_token: Optional[str] = None,
) -> Dict[str, Any]:
    headers = build_headers(access_token)
    headers["Content-Type"] = "application/json"

    json_data = {"model": model, "input": input_}

    return {
        "method": "POST",
        "url": "/tokens/count",
        "headers": headers,
        "json": json_data,
    }


async def _build_response(response: aiohttp.ClientResponse) -> List[TokensCount]:
    if response.status == HTTPStatus.OK:
        json_data = await response.json()
        return [TokensCount(**row) for row in json_data]
    elif response.status == HTTPStatus.UNAUTHORIZED:
        content = await response.read()
        raise AuthenticationError(str(response.url), response.status, content, response.headers)
    else:
        content = await response.read()
        raise ResponseError(str(response.url), response.status, content, response.headers)


def sync(
    client: aiohttp.ClientSession,
    *,
    input_: List[str],
    model: str,
    access_token: Optional[str] = None,
) -> List[TokensCount]:
    """Возвращает объект с информацией о количестве токенов"""
    kwargs = _get_kwargs(input_=input_, model=model, access_token=access_token)
    response = client.request(**kwargs)
    return _build_response(response)


async def asyncio(
    client: aiohttp.ClientSession,
    *,
    input_: List[str],
    model: str,
    access_token: Optional[str] = None,
) -> List[TokensCount]:
    """Возвращает объект с информацией о количестве токенов"""
    kwargs = _get_kwargs(input_=input_, model=model, access_token=access_token)
    async with client.request(**kwargs) as response:
        return await _build_response(response)
