import base64
from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import aiohttp
import requests

from gigachat.api.utils import build_headers, build_x_headers
from gigachat.exceptions import AuthenticationError, ResponseError
from gigachat.models import Image


def _get_kwargs(
    *,
    file_id: str,
    access_token: Optional[str] = None,
) -> Dict[str, Any]:
    headers = build_headers(access_token)
    headers["Accept"] = "application/jpg"
    return {
        "method": "GET",
        "url": f"/files/{file_id}/content",
        "headers": headers,
    }


def _build_response_sync(response: requests.Response) -> Image:
    if response.status_code == HTTPStatus.OK:
        x_headers = build_x_headers(response)
        content = response.content
        return Image(x_headers=x_headers, content=base64.b64encode(content).decode())
    elif response.status_code == HTTPStatus.UNAUTHORIZED:
        content = response.content
        raise AuthenticationError(str(response.url), response.status_code, content, response.headers)
    else:
        content = response.content
        raise ResponseError(str(response.url), response.status_code, content, response.headers)


async def _build_response_async(response: aiohttp.ClientResponse) -> Image:
    if response.status == HTTPStatus.OK:
        x_headers = build_x_headers(response)
        content = await response.read()
        return Image(x_headers=x_headers, content=base64.b64encode(content).decode())
    elif response.status == HTTPStatus.UNAUTHORIZED:
        content = await response.read()
        raise AuthenticationError(str(response.url), response.status, content, response.headers)
    else:
        content = await response.read()
        raise ResponseError(str(response.url), response.status, content, response.headers)


def sync(
    client: Union[aiohttp.ClientSession, requests.Session],
    *,
    file_id: str,
    access_token: Optional[str] = None,
) -> Image:
    """Возвращает изображение в base64 кодировке"""
    kwargs = _get_kwargs(access_token=access_token, file_id=file_id)
    response = client.request(**kwargs)
    return _build_response_sync(response)


async def asyncio(
    client: aiohttp.ClientSession,
    *,
    file_id: str,
    access_token: Optional[str] = None,
) -> Image:
    """Возвращает изображение в base64 кодировке"""
    kwargs = _get_kwargs(access_token=access_token, file_id=file_id)
    async with client.request(**kwargs) as response:
        return await _build_response_async(response)
