import json
from http import HTTPStatus
from typing import Any, AsyncIterator, Dict, Iterator, Optional, Union

import aiohttp
import requests

from gigachat.api.utils import build_headers, build_x_headers, parse_chunk
from gigachat.exceptions import AuthenticationError, ResponseError
from gigachat.models import Chat, ChatCompletionChunk

EVENT_STREAM = "text/event-stream"


def _get_kwargs(
    *,
    chat: Chat,
    access_token: Optional[str] = None,
) -> Dict[str, Any]:
    headers = build_headers(access_token)
    headers["Accept"] = EVENT_STREAM
    headers["Cache-Control"] = "no-store"
    headers["Content-Type"] = "application/json"

    return {
        "method": "POST",
        "url": "/chat/completions",
        "json": {**chat.dict(exclude_none=True, by_alias=True), **{"stream": True}},
        "headers": headers,
    }


def _check_content_type(response: Union[aiohttp.ClientResponse, requests.Response]) -> None:
    content_type, _, _ = response.headers.get("content-type", "").partition(";")
    if content_type != EVENT_STREAM:
        raise ValueError(f"Expected response Content-Type to be '{EVENT_STREAM}', got {content_type!r}")


def _check_response(response: requests.Response) -> None:
    if response.status_code == HTTPStatus.OK:
        _check_content_type(response)
    elif response.status_code == HTTPStatus.UNAUTHORIZED:
        raise AuthenticationError(str(response.url), response.status_code, response.content, response.headers)
    else:
        raise ResponseError(str(response.url), response.status_code, response.content, response.headers)


async def _acheck_response(response: aiohttp.ClientResponse) -> None:
    if response.status == HTTPStatus.OK:
        _check_content_type(response)
    elif response.status == HTTPStatus.UNAUTHORIZED:
        content = await response.read()
        raise AuthenticationError(str(response.url), response.status, content, response.headers)
    else:
        content = await response.read()
        raise ResponseError(str(response.url), response.status, content, response.headers)


def sync(
    client: Union[aiohttp.ClientSession, requests.Session],
    *,
    chat: Chat,
    access_token: Optional[str] = None,
) -> Iterator[ChatCompletionChunk]:
    kwargs = _get_kwargs(chat=chat, access_token=access_token)
    response = client.request(**kwargs)
    _check_response(response)
    x_headers = build_x_headers(response)
    for line in response.iter_lines():
        if line:
            if chunk := parse_chunk(line.decode(), ChatCompletionChunk):
                chunk.x_headers = x_headers
                yield chunk


async def asyncio(
    client: aiohttp.ClientSession,
    *,
    chat: Chat,
    access_token: Optional[str] = None,
) -> AsyncIterator[ChatCompletionChunk]:
    kwargs = _get_kwargs(chat=chat, access_token=access_token)
    async with client.request(**kwargs) as response:
        await _acheck_response(response)
        x_headers = build_x_headers(response)
        async for line in response.content.iter_any():
            if chunk := parse_chunk(line.decode(), ChatCompletionChunk):
                chunk.x_headers = x_headers
                yield chunk
